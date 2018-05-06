#use word2vec to tokenize the Japanese auther's arts
#download the files from Aozorabunko is necessarry
import os, re
from janome.tokenizer import Tokenizer

#Morphological analysis
def tokenize(text):
    t = Tokenizer()
    #delete header and footer
    text = re.split(r'\-{5,}',text)[2]
    text = re.split(r'底本:',text)[0]
    text = text.strip()
    #delete kana(japanese character)
    text = text.replace('|','')
    text = re.sub(r'《.+?》','',text)
    #delete comments
    text = re.sub(r'[#.+?]','',text)
    #process a line and a line
    lines = text.split("\r\n")
    results = []
    for line in lines:
        res = []
        tokens = t.tokenize(line)
        for tok in tokens:
            bf = tok.base_form
            if bf == "*": bf = tok.surface
            ps = tok.part_of_speech
            hinsi = ps.split(',')[0]
            if hinsi in ['名詞','動詞','形容詞','記号']:#add other parts, if you want to split sentences more types
                res.append(bf)
        l = " ".join(res)
        results.append(l)
    return results

#make dictionary type data
person = ['       ']# fill the space 
sakuhin_count = {}
for p in person:
    person_dir = "./text/" +p
    sakuhin_count[p] = 0
    results = []
    for sakuhin in os.listdir(person_dir):
        print(p,sakuhin)
        sakuhin_count[p] += 1
        sakuhin_file = person_dir + "/" + sakuhin
        try:
            #read the file of Shift_JIS
            bindata = open(sakuhin_file,"rb").read()
            text = bindata.decode("shift_jis")
            lines = tokenize(text)
            results += lines
        except Exception as e:
            print("[error]", sakuhin_file,e)
            continue
    #save it as file
    fname = "./text/" + p + ".wakati"
    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(p)

print("作品数:",sakuhin_count)
