import random
import re
import sqlite3
import sqlite3
def guess_game(number_range):
    num_list=[i for i in range(number_range)]
    current_num=random.choice(num_list)
    input_num=int(input("the number that you want to take a guess:"))
    guess_time=0
    while input_num!=current_num:
        guess_time+=1
        if input_num<current_num:
            print("please enter a bigger number")
        else:
            print("please enter a smaller number")
        input_num = int(input("the number that you want to take a guess:"))
    print(f"you got it! the correct number is {current_num} and you spent {guess_time} times")
def read_vocabbooks(path,encoding='utf-8'):
    with open(path,'r',encoding=encoding) as f:
        rows=f.readlines()
        content=[]
        for row in rows:
            elements_1=re.findall('[a-z]+',row)
            elements_2=re.findall('[a-z]+\..*',row)
            content.append([elements_1[0],elements_2[0]])
        return content
def read_csv(path,encoding="utf-8"):
    with open (path,encoding=encoding) as f:
        infor_list=[]
        for row in f.readlines():
            index=[0]#储存分离点：按照csv命名规则
            infor=[]#储存根据分离点提取的
            sign=True#储存分离点遇到“的形式
            num_double_quotes=0
            for i in range(len(row)):
                if (row[i] == '\"'):
                    num_double_quotes+=1
                    if num_double_quotes %2==1:
                        sign=False
                    else:
                        sign=True
                if (row[i] == ',' and sign) or (row[i]=="\"" and row[i+1]=="\n"):
                    index.append(i)
            for i in range(len(index)-1):
                information=row[index[i]:index[i+1]].replace(',','').replace('"','').replace("'","''")
                if information!='':
                    infor.append(information)
                else:
                    infor.append('notProvided')
            infor.append(row.split(',')[-1].replace(":","->"))
            infor_list.append(infor)
        del infor_list[0]
        return infor_list
def create_LowlevelExample_csvTable():
    infors=read_csv('DataForUse/LowLevelWordsExample.csv')
    sqliteConnection = sqlite3.connect('DataForUse/ecdictWords.db')
    cursor = sqliteConnection.cursor()
    num=0
    cursor.execute(f"drop table LowLevelWordsExample")
    cursor.execute('create table LowLevelWordsExample(id integer,word text,detail text);')
    for infor in infors:
        num+=1
        print(num)
        cursor.executemany("insert into LowLevelWordsExample(id,word,detail) VALUES(?,?,?)", zip({infor[0]}, {infor[1]}, {infor[2].replace('.','/.')}))
    sqliteConnection.commit()
    cursor.close()
def create_Lowlevel_csvTable():
    infors=read_csv('DataForUse/LowLevelWords.csv')
    sqliteConnection = sqlite3.connect('DataForUse/ecdictWords.db')
    cursor = sqliteConnection.cursor()
    num=0
    cursor.execute(f"drop table LowLevelWords")
    cursor.execute('create table LowLevelWords(id integer,word text,definition text,translation text,collins text,oxford text,tag text,bnc text,frq text,exchange text,detail text,audio text);')
    for infor in infors:
        num+=1
        print(num)
        print(infor)
        del infor[2]
        cursor.executemany("insert into LowLevelWords(id,word,definition,translation,collins,oxford,tag,bnc,frq,exchange,detail,audio) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", zip({infor[0]}, {infor[1]}, {infor[2].split(':')[1].replace('.','/.')}, {infor[3].split(':')[1].replace('.','/.')}, {infor[4].split(':')[1].replace('.','/.')}, {infor[5].split(':')[1].replace('.','/.')}, {infor[6].split(':')[1].replace('.','/.')}, {infor[7].split(':')[1].replace('.','/.')}, {infor[8].split(':')[1].replace('.','/.')}, {infor[9].split(':')[1].replace('.','/.')}, {infor[10].split(':')[1].replace('.','/.')}, {infor[11]}))
    sqliteConnection.commit()
    cursor.close()
def create_Middlelevel_csvTable():
    infors=read_csv('DataForUse/MiddleLevelWords.csv')
    sqliteConnection = sqlite3.connect('DataForUse/ecdictWords.db')
    cursor = sqliteConnection.cursor()
    num=0
    cursor.execute(f"drop table MiddleLevelWords")
    cursor.execute('create table MiddleLevelWords(id integer,word text,definition text,translation text,oxford text,tag text,bnc text,frq text,exchange text,detail text,audio text);')
    for infor in infors:
        num+=1
        del infor[2]
        cursor.executemany("insert into MiddleLevelWords(id,word,definition,translation,oxford,tag,bnc,frq,exchange,detail,audio) VALUES(?,?,?,?,?,?,?,?,?,?,?)", zip({infor[0]}, {infor[1]}, {infor[2].split(':')[1].replace('.','/.')}, {infor[3].split(':')[1].replace('.','/.')}, {infor[6].split(':')[1].replace('.','/.')}, {infor[7].split(':')[1].replace('.','/.')}, {infor[8].split(':')[1].replace('.','/.')}, {infor[9].split(':')[1].replace('.','/.')}, {infor[10].split(':')[1].replace('.','/.')},{infor[11].split(':')[1].replace('.','/.')},{infor[12]}))
    sqliteConnection.commit()
    cursor.close()
# create_Lowlevel_csvTable()
#create index!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def create_index():
    for i in ['MiddleLevelWords']:
        print(i)
        sqliteConnection = sqlite3.connect('DataForUse/ecdictWords.db')
        cursor = sqliteConnection.cursor()
        cursor.execute(f"create index {i}_id on {i}(id,word)")
        sqliteConnection.commit()
        cursor.close()

