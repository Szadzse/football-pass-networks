import re
import os

def search_GK(fname,ev):
    pattern = re.compile(r'^.*GK$')
    ok = 0
    #print('data/input/'+str(ev)+'/'+fname)
    with open('data/input/'+str(ev)+'/'+fname, 'r', encoding='utf-8') as f:
        for line in f:
            if pattern.match(line) and ok==1:
                secondGK = re.sub(r'\d+|GK', '', line)
                #secondGK= line.lstrip()
                ok = ok+1
            if pattern.match(line) and ok==0:
                firstGK = re.sub(r'\d+|GK', '', line)
                #firstGK= line.lstrip()
                ok = ok+1
            if ok == 2:
                break
    return firstGK, secondGK


def vag(fname, secondGK, ev):
    ok = 0
    kk = 0
    tpr = 0

    input_file = open('data/input/'+str(ev)+'/'+fname, 'r', encoding='utf-8')
    outfname = re.search(r'^(\d+)_', fname).group(1)
    #outfname = re.sub(r'^\d+_', '', fname)
    #print('data/processed/'+str(ev)+'/'+ outfname+'.txt',)
    output_file = open('data/processed/'+str(ev)+'/'+ outfname+'.txt', 'w', encoding='utf-8')
    

    for line in input_file:
        if ok == 1 and line.count(" ") >= 8 :
            output_file.write(line.replace('-', '0'))
        else:
            ok =0
        if line.strip() == "Long":
            output_file.write("First team:\n")
            ok = 1
        if tpr == 1 and line.count(" ") >= 8 and not line.startswith("Total passes received:") :
            output_file.write(line.replace('-', '0'))
        if tpr == 2:
            #eltávolíto, a string elejéről az összes whitespace karaktert
            if secondGK.strip() == line.strip():
                output_file.write("Second team players:\n")
                
            output_file.write(line.lstrip())
        if line.startswith("Total passes received:"):
            tpr = tpr + 1
            if tpr == 1:
                output_file.write("Second team:\n")
            if tpr == 2:
                output_file.write("Players:\n")
                output_file.write("First team players:\n")

    input_file.close()
    output_file.close()

def main(ev):
    path = "data/input/" + str(ev)  # helyettesítsd a mappa elérési útjával
    itt = 0
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            #print(str(itt) + ' ' + filename )
            if itt == 2:
                itt = itt+1
            if itt == 1:
                vag(filename, secondGK, ev)
                itt = itt+1
            if itt == 0:
                firstGK, secondGK = search_GK(filename,ev)
                itt = itt+1
            itt = itt % 3
    print(str(ev) + " ev kesz!")

            
            

#main(2020)
main(2021)
main(2022)
main(2023)



