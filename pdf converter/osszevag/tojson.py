import re
import os
import json

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


def create_json(matrix1,matrix2,fplayer,splayer,fname):
    data = {
        "fmatrix": matrix1,
        "smatrix": matrix2,
        "fplayers": fplayer,
        "splayers": splayer
    }

    json_data = json.dumps(data, ensure_ascii=False)
    
    # JSON fájlba írás
    with open(fname, 'w',  encoding='utf-8') as f:
        f.write(json_data)


def vag(fname, secondGK, ev):
    ok = 0
    tpr = 0
    matrix1 = []
    row_count1 = 0
    matrix2 = []
    row_count2 = 0
    fplayer = []
    splayer = []

    input_file = open('data/input/'+str(ev)+'/'+fname, 'r', encoding='utf-8')
    outfname = re.search(r'^(\d+)_', fname).group(1)
    print('data/processed2/'+str(ev)+'/'+ outfname+'.json',)
    output_file = 'data/processed2/'+str(ev)+'/'+ outfname+'.json'
    

    for line in input_file:
        if ok == 1 and line.count(" ") >= 8 :
            row_count1 += 1
            matrix_row = list(map(int, line.replace('-', '0').split()))
            matrix_row.insert(row_count1 - 1, -1)
            matrix1.append(matrix_row)
        else:
            ok =0
        if line.strip() == "Long":
            ok = 1
        if tpr == 1 and line.count(" ") >= 8 and not line.startswith("Total passes received:") :
            row_count2 += 1
            matrix_row = list(map(int, line.replace('-', '0').split()))
            matrix_row.insert(row_count2 - 1, -1)
            matrix2.append(matrix_row)
        if tpr == 2:
            if secondGK.strip() == line.strip():
                fplayer = splayer
                splayer = []
            splayer.append(line.lstrip().strip())
        if line.startswith("Total passes received:"):
            tpr = tpr + 1


    input_file.close()
    #print(matrix1)
    #print(matrix2)
    #print(fplayer)
    splayer.pop()
    #print(splayer)
    create_json(matrix1,matrix2,fplayer,splayer,output_file)

def main(ev):
    path = "data/input/" + str(ev)  
    itt = 0
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
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
#main(2021)
#main(2022)
#main(2023)
main(2019)


