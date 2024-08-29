import re

def search_GK(fname):
    pattern = re.compile(r'^.*GK$')
    ok = 0
    with open(fname, 'r', encoding='utf-8') as f:
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


def vag(fname):
    ok = 0
    kk = 0
    tpr = 0
    matrix1 = []
    row_count1 = 0
    matrix2 = []
    row_count2 = 0

    input_file = open(fname, 'r', encoding='utf-8')
    outfname = re.search(r'^(\d+)_', fname).group(1)
    #outfname = re.sub(r'^\d+_', '', fname)
    print(outfname)
    output_file = open(outfname+'.txt', 'w', encoding='utf-8')
    

    for line in input_file:
        if ok == 1 and line.count(" ") >= 8 :
            output_file.write(line.replace('-', '0'))
            row_count1 += 1
            matrix_row = list(map(int, line.replace('-', '0').split()))
            matrix_row.insert(row_count1 - 1, -1)
            matrix1.append(matrix_row)
        else:
            ok =0
        if line.strip() == "Long":
            output_file.write("First team:\n")
            ok = 1
        if tpr == 1 and line.count(" ") >= 8 and not line.startswith("Total passes received:") :
            output_file.write(line.replace('-', '0'))
            row_count2 += 1
            matrix_row = list(map(int, line.replace('-', '0').split()))
            matrix_row.insert(row_count2 - 1, -1)
            matrix2.append(matrix_row)
        if tpr == 2:
            #eltávolíto, a string elejéről az összes whitespace karaktert
            #if secondGK.strip() == line.strip():
            #    output_file.write("Second team players:\n")
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
    print(matrix1)
    print(matrix2)

def main():
    #firstGK, secondGK = search_GK('2036582_lu.txt')
    #print(firstGK, secondGK)
    vag('2036582_tpd.txt')

main()