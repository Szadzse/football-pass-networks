import re

pattern = re.compile(r'^.*GK$')
ok = 0

with open('2036582_lu.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if pattern.match(line) and ok == 0:
            ok = 1
        if ok>0:
            print(line.strip())
            ok = ok+1
        if ok > 22:
            break
