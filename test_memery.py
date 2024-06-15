import sqlite3
from random import choice
from crawlerfile.request_Dictionarycom import *
from crawlerfile.request_YouDao import *

class test_memery:
    def __init__(self,name,filepath) -> None:
        self.database_1="DataForUse/test_memery.db"
        self.database_2="DataForUse/ecdictWords.db"
        self.name=name
        self.filepath=filepath
    def initiallize_all(self):
        con = sqlite3.connect(self.database_1)
        with con:
            cur = con.cursor()  
            cur.execute(f"Drop table test_learning;")
            con.commit()
        os.remove("test_memory\STUDY_VOCABULARY.txt")

    def init_program(self,initiallize_all=False)->None:
        con = sqlite3.connect(self.database_1)
        with con:
            cur = con.cursor()
            try:
                cur.execute(f"CREATE TABLE {self.name}(id int,word text,correct_time integer,wrong_time integer,phonetic text ,definition text,translation text,collins text,oxford text,tag text,bnc text,frq text ,exchange text ,detail text)")
                cur.execute(f"create index {self.name}_id on {self.name}(word,correct_time,wrong_time,detail,definition,translation)")
                con.commit()
                cur.close
            except:
                pass
        if initiallize_all:
            initiallize_all()
    #if you want to pass the parameter"filename" you should enter a word each line
    def add_words(self,threadNum=10)->None:
        import threading
        threadList=list()
        con_1 = sqlite3.connect(self.database_1)
        with con_1 :
            cur = con_1.cursor()
            cur.execute(f"SELECT word From {self.name};")
            word_stored=cur.fetchall()
            for i in range(len(word_stored)):
                word_stored[i]=list(word_stored[i])[0].replace("\n","")
        words=[]
        with open(self.filepath,'r') as f:
            for word in f.readlines():
                try:
                    word=word.split(":")[1]
                except:
                    pass
                word=word.strip('\r\n\t ')
                if word not in word_stored and word!='':
                    words.append(word)
        word_infors=[]
        print(f"going to process {len(words)} times since you have sent us {len(words)} words ,please be patient")
        print(f"they are {words}")
        def processwords(words,threadNUmber):
            for i in range(round((threadNUmber)*len(words)/threadNum),
            round((threadNUmber+1)*len(words)/threadNum)):
                print_string=''
                con_2=sqlite3.connect(self.database_2)
                cur_2 = con_2.cursor()
                cur_2.execute(f"SELECT word,definition,translation,oxford,tag,bnc,frq,exchange,detail From MiddleLevelWords where word='{words[i]}'")
                word_infor=cur_2.fetchone()
                if word_infor==None:
                    continue
                word_infor=list(word_infor)
                ob=YouDao_search()
                infor_1=ob.YouDao_search_example_sentences(words[i])+"\n"
                print(f"youdao finish searching word {words[i]}")
                infor_2=request_Dictionarycom(words[i])+"\n"
                print(f"Dictionarycom finish searching word {words[i]}")
                infor_3=request_Longman(words[i])+"\n"
                print(f"longman finish searching word {words[i]}")
                infor_4=example_sentence(words[i])+"\n"
                print(f"Example-king! finish searching word {words[i]}")           
                print_string=infor_1+infor_2+infor_3+infor_4
                if len(print_string)>=2700:
                    print_string=print_string[:2700]
                word_infor[-1]=print_string
                for i in range(len(word_infor)):
                    word_infor[i]=word_infor[i].replace("'","''")+"\n"
                word_infors.append(word_infor)
                con_1=sqlite3.connect(self.database_1)
                cur_1 = con_1.cursor()
                if word_infor[2]!=word_infor[3]:
                    cur_1.execute(f"insert into {self.name}(word,correct_time,wrong_time,definition,translation,oxford,tag,bnc,frq,exchange,detail) values('%s',0,0,'%s','%s','%s','%s','%s','%s','%s','%s');"%tuple(word_infor))
                    con_1.commit()
            with open(f'exported_wordList\\STUDY_{self.name}.txt','a',encoding='utf-8') as f:
                for word_infor in word_infors:
                    for infor in word_infor:
                        f.write(infor.replace("''","'")+" ")
        for i in range(0,threadNum):
            threadList.append(threading.Thread(target=processwords(words,i)))
            threadList[i].start()
    #generate test to test proficiency      
    def test_proficiency(self)->None:
        con = sqlite3.connect(self.database_1)
        with con:
            cur = con.cursor()    
            word_num=0
            while word_num!=15:
                cur.execute(f"select word,definition,translation,correct_time,wrong_time from {self.name} where correct_time-wrong_time<=2")
                testwords_list=cur.fetchall()
                current_word_list=choice(testwords_list)
                if current_word_list[1].replace("\n","")=='definition: 1.notProvided':
                    current_test_word=str(input(f"what is the word that means {current_word_list[2]}"))
                else:
                    current_test_word=str(input(f"what is the word that means {current_word_list[1]}"))
                if current_test_word.replace("\n","")==current_word_list[0].replace("\n",""):
                    print("congrats! you are correct")
                    cur.execute(f"Update {self.name} set correct_time={int(current_word_list[3])+1} where word='{current_word_list[0]}';")
                    con.commit()
                else :
                    print(f"Wrong try again! the correct answer is {current_word_list[0]}")
                    cur.execute(f"Update {self.name} set wrong_time={int(current_word_list[4])+1} where word='{current_word_list[0]}';")
                    con.commit()
                word_num+=1
                if word_num==15:
                    a=input("want to exit test mode?(y/n):")
                    if a.lower()!='y':
                        word_num=0

    def delete_word(self,word):
        con = sqlite3.connect(self.database_1)
        with con:
            cur = con.cursor()  
            cur.execute(f"delete from {self.name} as test where test.word='{word}\n';")
            con.commit()
            print(f"finish deleting the word {word}")

    def show_data(self):
        con = sqlite3.connect(self.database_1)
        with con:
            cur=con.cursor()
            cur.execute(f"select word,definition,translation,correct_time,wrong_time from {self.name} order by (correct_time-wrong_time)")
            inforList=cur.fetchall()
            with open("exported_wordList\\current_word_data.txt","w") as f:
                for infor in inforList:
                    f.write(infor[0])
                    f.write(infor[1])
                    f.write(infor[2])
                    f.write(f"correctly answer time: {infor[3]}\n")
                    f.write(f"wrongly answer time: {infor[4]}\n\n")


if __name__=="__main__":
    #项目简介：传入目标txt文件路径，生成数据库（在DataForUse目录下）并生成超多例句的文件：STUDY_xxxx（在exported_wordlist下）
    # 在控制台进行检测单词背诵情况，默认为一个单词正确数量超过错误数量2个时不再进行检测
    #默认生成一个txt文件看进度，在exported_wordlist目录下，文件名为current_word_data
    #txt格式为每行一个单词单独出现，或者WORD:单词这种形式（第二种格式主要为了匹配我的另一个项目：读取书生成词单
    test1=test_memery("test2","exported_wordList\\test.txt")#第一个参数是选择建立table的名称：xxxx，第二个是选择导入txt文件的路径
    test1.init_program()#初始化table
    test1.add_words()#读取txt文件，并用网络爬虫生成超多例句文件STUDY_xxxx
    test1.show_data()#默认生成一个txt文件
    test1.test_proficiency()#开始测试
    

