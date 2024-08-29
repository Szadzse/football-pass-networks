import re
import os
import json

keys = ['Goals_scored', 'Total_attemps','One_target','Off_target','Blocked','Woodwork','Saves','Corners','Offsides','Total_time_played','Ball_possession','Distance_covered','Yellow_cards','Red_cards','Fouls_committed','Fouls_suffered','Passes_attemted','Short_Passes_attemted','Medium_Passes_attemted','Long_Passes_attemted','Passes_completed','Short_Passes_completed','Medium_Passes_completed','Long_Passes_completed','Pass_completion_rate','Short_rate','Medium_rate','Long_rate','Into_the_attacking_third','Into_the_key_area','Into_the_penalty_area']
keys2 = ['Goals_scored', 'Total_attemps','One_target','Off_target','Blocked','Woodwork','Saves','Corners','Offsides','Total_time_played','Ball_possession','Yellow_cards','Red_cards','Fouls_committed','Fouls_suffered','Passes_attemted','Short_Passes_attemted','Medium_Passes_attemted','Long_Passes_attemted','Passes_completed','Short_Passes_completed','Medium_Passes_completed','Long_Passes_completed','Pass_completion_rate','Short_rate','Medium_rate','Long_rate','Into_the_attacking_third','Into_the_key_area','Into_the_penalty_area']

def main(ev):
    path = "./data/input/" + str(ev)  
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

#main(2020)
def firts():
    with open('./data/input/2020/2027013_ts.txt', 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            num_count = 0
            for word in words:
                if word.isdigit():
                    num_count += 1
            if num_count == 3:
                print(line)

def proces_file(filename):
    first_data =[]
    second_data = []

    with open(filename, 'r', encoding='utf-8') as f:
        found = False
        found1 = True
        found2 =False
        for line in f:
            if "Attacking" in line:
                found = False
                found1 = False
            if "First half" in line:
                break
            line = line.rstrip()
            words = line.strip().split()
            num_count = 0
            for word in words:
                if word.isdigit():
                    num_count += 1
            if num_count == 3 and not found and found1:
                found = True
            if found :
                first_data.append(line)
            if num_count == 3 and not found2 and not found1:
                found2 = True
            if found2 :
                second_data.append(line)

    return first_data,second_data
                
def firts():
    with open('./data/input/2020/2027013_ts.txt', 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            num_count = 0
            for word in words:
                if word.isdigit():
                    num_count += 1
            if num_count == 3:
                print(line)

def proces_file2(filename):
    first_data =[]
    second_data = []
    last_line = ''
    with open(filename, 'r', encoding='utf-8') as f:
        #found = False
        found1 = False
        #found2 =False
        count = 0
        l1 = []
        l2 = []
        l11 = []
        l22 = []
        l111 = []
        l222 = []
        for line in f:
            if len(line)>2:
                last_line = line.rstrip()
            if found1:
                count = count+1
                #print(line)
                line = line.rstrip()
                if count <=29:
                    l1.append(line)
                elif count>29 and count<=58:
                    l2.append(line)
                elif count>58 and count<=87:
                    l11.append(line)
                elif count>87 and count<=116:
                    l22.append(line)
                elif count>116 and count<=145:
                    l111.append(line)
                elif count>145 and count<=174:
                    l222.append(line)

            if "Into the penalty area" in line:
                found1 = True
            if "First half" in line:
                found1 = False

    print(len(l1),len(l11),len(l111))
    print(len(l2),len(l22),len(l222))
    first_data = [ l1[i] + ' ' + l11[i] + ' ' + l111[i] for i in range(len(l1))]
    second_data = [ l2[i] +' '+ l22[i] + ' ' + l222[i] for i in range(len(l2))]
    return first_data,second_data,last_line

def proces_file3(filename):
    first_data =[]
    second_data = []

    with open(filename, 'r', encoding='utf-8') as f:
        found = False
        found1 = True
        found2 =False
        for line in f:
            if "Attacking" in line:
                found = False
                found1 = False
            if "First half" in line:
                break
            line = line.rstrip()
            words = line.strip().split()
            num_count = 0
            for word in words:
                if word.isdigit():
                    num_count += 1
            if num_count == 4 and not found and found1:
                found = True
            if found :
                first_data.append(line)
            if num_count == 4 and not found2 and not found1:
                found2 = True
            if found2 :
                second_data.append(line)

    return first_data,second_data
   
def print_to_json(first_data,second_data,outfname, keys):
    print(len(first_data),len(second_data),len(keys))
    if len(first_data) == len(second_data) == len(keys):
        print(outfname)
    else:
        return

    data1 = {}
    for i in range(len(keys)):
        data1[keys[i]] = first_data[i]

    data2 = {}
    for i in range(len(keys)):
        data2[keys[i]] = second_data[i]

    data = {}
    data['FirstTeam']=data1
    data['SecondTeam']=data2
    with open(outfname, "w") as f:
        json.dump(data, f)

    #print(data)


def megold1(ev):
    path = "data/input/" + str(ev)  
    itt = 0
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            if itt == 2:
                itt = itt+1
                outfname = re.search(r'^(\d+)_', filename).group(1)
                output_file = 'data/output/'+str(ev)+'/'+ outfname+'.json'
                input_file = './data/input/'+str(ev)+'/'+filename
                first_data,second_data = proces_file(input_file)
                print(len(first_data), len(second_data))
                if (len(first_data) != 30 or len(second_data) != 30):
                    first_data,second_data,ll = proces_file2(input_file)
                    first_data.insert(9,ll)
                    second_data.insert(9,ll)
                
                
                print_to_json(first_data,second_data,output_file,keys)
            if itt == 1:
                #vag(filename, secondGK, ev)
                itt = itt+1
            if itt == 0:
                #firstGK, secondGK = search_GK(filename,ev)
                itt = itt+1
            itt = itt % 3
    print(str(ev) + " ev kesz!")

def megold2(ev):
    path = "data/input/" + str(ev)  
    itt = 0
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            if itt == 2:
                itt = itt+1
                outfname = re.search(r'^(\d+)_', filename).group(1)
                output_file = 'data/output/'+str(ev)+'/'+ outfname+'.json'
                input_file = './data/input/'+str(ev)+'/'+filename
                first_data,second_data = proces_file(input_file)
                print(len(first_data), len(second_data))
                if (len(first_data) != 30 or len(second_data) != 30):
                    first_data,second_data = proces_file3(input_file)
                    #first_data,second_data,ll = proces_file2('./data/input/2020/2027024_ts.txt')
                    #first_data.insert(9,ll)
                    #second_data.insert(9,ll)
                if (len(first_data) != 30 or len(second_data) != 30):
                    first_data,second_data,ll = proces_file2(input_file)
                    first_data.insert(9,ll)
                    second_data.insert(9,ll)
                print_to_json(first_data,second_data,output_file,keys2)
                #if (output_file == 'data/output/2022/2032640.json'):
                    #print(first_data,second_data)
                #    print('kilepes')
                #    exit()
            if itt == 1:
                #vag(filename, secondGK, ev)
                itt = itt+1
            if itt == 0:
                #firstGK, secondGK = search_GK(filename,ev)
                itt = itt+1
            itt = itt % 3
    print(str(ev) + " ev kesz!")


def main(ev):
    if(ev<2022):
        megold1(ev)
    else:
        megold2(ev)


#first_data,second_data = proces_file('./data/input/2020/2027013_ts.txt')
#print_to_json(first_data,second_data)

#main(2020)
#main(2021)
main(2022)
main(2023)

#first_data,second_data,ll = proces_file2('./data/input/2020/2027024_ts.txt')
#first_data.insert(9,ll)
#second_data.insert(9,ll)
#print_to_json(first_data,second_data,'./kecske.json')