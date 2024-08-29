import re
import os

def main(ev):
    path = "data/input/" + str(ev)  
    itt = 0
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            if itt == 2:
                itt = itt+1
                print(filename)
            if itt == 1:
                #vag(filename, secondGK, ev)
                itt = itt+1
            if itt == 0:
                #firstGK, secondGK = search_GK(filename,ev)
                itt = itt+1
            itt = itt % 3
    print(str(ev) + " ev kesz!")

main(2020)