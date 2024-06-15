##TO DO:
# add a text displaying all the textbooks in the window
# add more thread so that it could process faster
# seperate the big study vocabulary list into smaller one and sign on days for it to be remembered
# adding more example sentences!
import time
import tkinter
from tkinter import *
from random import choice
import sqlite3
from re import findall,sub
from tkinter import *
from tkinter import messagebox
from os import walk
import os
from tkinter.ttk import *
import pdfplumber
current_novel=''
current_vocablist=''
#btn_1
#背单词功能----------------------------------------------------------------------------------
def choose_vocaList():
    def set_current_list(table_list,chooseVocabPage,table_list_text):
        global current_vocablist
        val = table_list_text.get(table_list_text.curselection())
        try:
            current_vocablist = table_list[int(val.split(".")[0][2])-1][0]
            print(f"current_vocablist is {current_vocablist}")
            messagebox.showinfo("success",f"已经选择{current_vocablist}")
        except:
            messagebox.showinfo("empty input","无对应选项")
        chooseVocabPage.destroy()
    def delete_vocablist(table_list,chooseVocabPage,table_list_text):
        con = sqlite3.connect('DataForUse/VocabList_database.db')
        cur = con.cursor()
        #select * from sqlite_master where type='table'
        val = table_list_text.get(table_list_text.curselection())
        val=table_list[int(val.split(".")[0][2])-1][0]
        cur.execute(f"Drop table {val}")
        con.commit()
        cur.close()
        messagebox.showinfo("success!",f"successfully delete table {val}")
        chooseVocabPage.destroy()
        run_choose_vocaList()
    def run_choose_vocaList():
        chooseVocabPage = Tk()
        chooseVocabPage.title("选择要背的词表")
        chooseVocabPage.geometry('300x300')
        con = sqlite3.connect('DataForUse/VocabList_database.db')
        cur = con.cursor()
        #select * from sqlite_master where type='table'
        cur.execute("SELECT name _id FROM sqlite_master WHERE type ='table';")
        table_list=cur.fetchall()
        table_list_text = Listbox(chooseVocabPage, height=10, width=40,selectmode="single")
        table_list_text.pack(side='top')
        table_num=0
        for table_name in table_list:
            table_num+=1
            table_list_text.insert(tkinter.END, f"词单{table_num}.{table_name[0]}\n")
        buttom_finish=Button(chooseVocabPage,text="完成选择",command=lambda:set_current_list(table_list,chooseVocabPage,table_list_text))
        buttom_finish.pack(side='bottom')
        buttom_delete=Button(chooseVocabPage,text="删除词单",command=lambda:delete_vocablist(table_list,chooseVocabPage,table_list_text))
        buttom_delete.pack(side="bottom")
        instruction=Label(chooseVocabPage,text="单击选择列表里的词单\n完成选择后点击完成选择\n或点击删除词单删除词单")
        instruction.pack(side='bottom')
    run_choose_vocaList()

def start_remembering():
    def run_start_remembering():
        def insert_without(param):
            #数据库部分
            mylist.delete("1.0","end")
            con_1 = sqlite3.connect('DataForUse/VocabList_database.db')
            cur_1 = con_1.cursor()
            cur_1.execute(f"select word,definition,translation,bnc,frq,fetched_level from {current_vocablist} order by fetched_level,frq desc")
            inforList=cur_1.fetchall()
            import threading
            t1=threading.Thread
            for infor in (inforList):
                if param=="definition":
                    mylist.insert(END,f"\nWORD:{infor[0]}\n")
                    mylist.insert(END, f"translation:{infor[2]}\n")
                    mylist.insert(END, f"bnc:{infor[3]}\n")
                    mylist.insert(END, f"frq:{infor[4]}\n")
                if param=="translation":
                    mylist.insert(END,f"\nWORD:{infor[0]}\n")
                    mylist.insert(END,f"definition:{infor[1]}\n")
                    mylist.insert(END, f"bnc:{infor[3]}\n")
                    mylist.insert(END, f"frq:{infor[4]}\n")
                if param=="both":
                    mylist.insert(END,f"\nWORD:{infor[0]}\n")
                if param=="restore":
                    mylist.insert(END,f"\nWORD:{infor[0]}\n")
                    mylist.insert(END,f"definition:{infor[1]}\n")
                    mylist.insert(END, f"translation:{infor[2]}\n")
                    mylist.insert(END, f"bnc:{infor[3]}\n")
                    mylist.insert(END, f"frq:{infor[4]}\n") 
        def view_zero():
            mylist.delete("1.0","end")
            con_1 = sqlite3.connect('DataForUse/VocabList_database.db')
            cur_1 = con_1.cursor()
            con_2 = sqlite3.connect('DataForUse/ecdictWords.db')
            cur_2 = con_2.cursor()
            cur_1.execute(f"select word,definition,translation,bnc,frq,fetched_level from {current_vocablist} order by frq,bnc asc")
            inforList=cur_1.fetchall()

            for infor in (inforList):
                mylist.insert(END,f"\nWORD:{infor[0]}\n")
                mylist.insert(END,f"definition:{infor[1]}\n")
                mylist.insert(END, f"translation:{infor[2]}\n")
                mylist.insert(END, f"bnc:{infor[3]}\n")
                mylist.insert(END, f"frq:{infor[4]}\n")
        def export_current_list(a):
            try:
                os.mkdir("exported_wordList")
            except:
                pass
            with open(f"exported_wordList\\{current_vocablist}.txt","w") as f:
                f.write(a)
                f.close()
            messagebox.showinfo("success",f"成功导出{current_vocablist}于exported_wordList文件夹")
        global current_vocablist
        if len(current_vocablist)==0:
            messagebox.showwarning("warning","你还没有选择相应的词单！")
        else:
            homepage_1=Tk()
            homepage_1.title("word-learner homepage")
            homepage_1.geometry('850x800')
            Notice=Label(homepage_1,text="NO definition button means showing the words without the english definitions\nSo do no translations\nNo both button means showing words without both difinitions and translations\nrestore button means back to the original version\nview word from bottom button means showing the word with ascendent order only in the original version",font=('times',15,"italic"))
            Notice.pack(side="top")
            scroll_bar = Scrollbar(homepage_1)
            scroll_bar.pack(side=RIGHT,fill=Y)
            mylist = Text(homepage_1,yscrollcommand=scroll_bar.set,width=3,height=30,background="Wheat",font='BahnschriftLight')
            mylist.pack(side='bottom', fill=BOTH)
            no_def=Button(homepage_1,text="no definition",command=lambda:insert_without("definition"))
            no_def.pack(side="left")
            no_trans=Button(homepage_1,text="no translation",command=lambda:insert_without("translation"))
            no_trans.pack(side="left")
            no_both=Button(homepage_1,text="no both",command=lambda:insert_without("both"))
            no_both.pack(side="left")
            restore=Button(homepage_1,text="restore",command=lambda:insert_without("restore"))
            restore.pack(side="left")
            viewZero=Button(homepage_1,text="view word from bottom",command=lambda:view_zero())
            viewZero.pack(side="left")
            export=Button(homepage_1,text="export the current list to a text",command=lambda:export_current_list(mylist.get("1.0","end")))
            export.pack(side="left")
            #数据库部分(默认)
            insert_without("restore")
    run_start_remembering()

def test_memery():
    if len(current_vocablist) == 0:
        messagebox.showwarning("warning", "你还没有选择相应的词单！")
    else:
        def test_proficiency():
            afbf=[]
            current_word_list_correcttime=[]
            con2 = sqlite3.connect('DataForUse/VocabList_database.db')
            with con2:
                #main graph
                cur = con2.cursor()
                def check_question(input_frame):
                    if input_frame.get() == afbf[-1]:
                        messagebox.showwarning("congrats", f"you spell the {afbf[-1]} correctly")
                        cur.execute(f"Update {current_vocablist} set correct_time={current_word_list_correcttime[-1] + 1});")
                    else:
                        messagebox.showwarning("sorry", f"the correct answer is {afbf[-1]}")
                    input_frame.delete(1,"end")
                    mylist.insert(END,"\nNEXT\n")
                def generate_question_ENG():
                    cur.execute(
                            f"select word,definition,translation,correct_time,wrong_time from {current_vocablist} where correct_time-wrong_time<=2")
                    testwords_list = cur.fetchall()
                    current_word_list = choice(testwords_list)
                    if current_word_list[1] == ' 1/.notProvided':
                        mylist.insert(END,str(current_word_list[2]))
                    else:
                         mylist.insert(END, str(current_word_list[1]))
                    mylist.insert(END, "\n")
                    afbf.append(current_word_list[0])
                    current_word_list_correcttime.append(current_word_list[3])
                def generate_question():
                    cur.execute(
                        f"select word,definition,translation,correct_time,wrong_time from {current_vocablist} where correct_time-wrong_time<=2")
                    testwords_list = cur.fetchall()
                    current_word_list = choice(testwords_list)
                    if current_word_list[1] == ' 1/.notProvided':
                        mylist.insert(END,str(current_word_list[2]))
                    else:
                        mylist.insert(END, str(current_word_list[1]))
                        mylist.insert(END,str(current_word_list[2]))
                    mylist.insert(END, "\n")
                    afbf.append(current_word_list[0])
                    current_word_list_correcttime.append(current_word_list[3])
                homepage_2=Tk()
                homepage_2.title("word-learner homepage")
                homepage_2.geometry('850x800')
                input_frame_1 = Entry(homepage_2, font=('times',20,"italic"),width=15)
                input_frame_1.pack(side="top")
                btn_frame_1=Button(homepage_2,text="click to check answer",command=lambda :check_question(input_frame_1))
                btn_frame_1.pack(side="top")
                btn_frame_2=Button(homepage_2,text="click to generate a new question with EnglishONLY",command=lambda :generate_question_ENG())
                btn_frame_2.pack(side="top",) 
                btn_frame_2=Button(homepage_2,text="click to generate a new question",command=lambda :generate_question())
                btn_frame_2.pack(side="top")
                scroll_bar = Scrollbar(homepage_2)
                scroll_bar.pack(side=RIGHT, fill=Y)
                mylist = Text(homepage_2, yscrollcommand=scroll_bar.set, width=20, height=30, background="Wheat",font='BahnschriftLight')
                mylist.pack(side='top', fill=BOTH)
                mylist.insert(1,"WHERE QUESTIONS SHOW\n")

            #前后匹配的词组
        test_proficiency()

#传单词书生成词单-----------------------------------------------------------------------------------------------
def read_vocabbooks(path, encoding='utf-8'):
    '''read vocabulary books with the same format'''
    with open(path, 'r', encoding=encoding) as f:
        rows = f.readlines()
        content = []
        for row in rows:
            elements_1 = findall('[a-z]+', row)
            elements_2 = findall('[a-z]+\..*', row)
            try:
                content.append([ elements_1[0], elements_2[0]])
            except(IndexError):
                pass
        return content
##从目录内置单词书获取数据，选择书导入
#单词类
def process_words_withDef(words_list,table_name,countTotal,threadNum=10):
    '''turn a book's word into the database'''
    from threading import Thread
    threadLIst=list()
    con = sqlite3.connect('DataForUse/ecdictWords.db')
    cur = con.cursor()
    cur.execute("SELECT name _id FROM sqlite_master WHERE type ='table';")
    table_list = cur.fetchall()
    if not table_name in table_list:
        new_words_list=[]
        sqliteConnection = sqlite3.connect('DataForUse/ecdictWords.db')
        cursor = sqliteConnection.cursor()
        global count
        count=0
        def looping_thread(words_list,cursor,new_words_list,threadId,threadTotal):
            global count
            for word_index in range(round(threadId*len(words_list)/threadTotal),round((threadId+1)*len(words_list)/threadTotal)):
                cursor.execute(f"Select id,word,definition,bnc,frq from LowLevelWords where word='{words_list[word_index][0]}'")
                first_fetch=cursor.fetchall()
                if len(first_fetch)==0:
                    cursor.execute(f"Select id,word,definition,bnc,frq from MiddleLevelWords where word='{words_list[word_index][0]}'")
                    second_fetch=cursor.fetchall()
                    if len(second_fetch)!=0:
                        infor=second_fetch[0]
                        new_words_list.append([infor[0],infor[1],infor[2],words_list[word_index][1],int(infor[3].replace("notProvided",'0')),int(infor[4]),2])
                else:
                    infor=first_fetch[0]
                    new_words_list.append([infor[0],infor[1],infor[2],words_list[word_index][1],int(infor[3].replace("notProvided",'0')),int(infor[4]),1])
                count=count+1
                print(f"have progressed {count*100/countTotal}%")
        start=time.time()
        for threadId in range(10):
            threadLIst.append(Thread(target=looping_thread(words_list,cursor,new_words_list,threadId,threadNum)))
            print(f"thread {threadId} start")
            threadLIst[threadId].start()
        end=time.time()
        print(f"total cost {start-end} second")
        sqliteConnection = sqlite3.connect('DataForUse/VocabList_database.db')
        cursor = sqliteConnection.cursor()
        table_name=sub('\(.*\)','',table_name)
        print(f"the table name is {table_name}")
        try:
            cursor.execute(f"drop table {table_name}")
        except:
            pass
        cursor.execute(f"create table {table_name}(id int,word text,definition text,translation text,bnc int,frq int,correct_time int,wrong_time int,fetched_level int)")
        for words_list in new_words_list:
            print(f"{words_list} inserted to {table_name}")
            cursor.executemany(f"insert into {table_name} (id,word,definition,translation,bnc,frq,correct_time,wrong_time,fetched_level) values(?,?,?,?,?,?,?,?,?)",zip((words_list[0],),(words_list[1],),(words_list[2],),(words_list[3],),(words_list[4],),(words_list[5],),(0,),(0,),(words_list[6],)))
        sqliteConnection.commit()
        cursor.close()
        return end-start

def choose_defaulVocabbook():
    def create_vocabList(vocabbooks_list,selector,root,choosevocabbooks):
        name=str(vocabbooks_list[int(selector.get()) - 1]).split('.')[0]
        path = str(root)+"/"+vocabbooks_list[int(selector.get()) - 1]
        infors=read_vocabbooks(path)
        messagebox.showinfo("warning", f"本文件将加载关于{len(infors)}个单词的信息，请耐心等待\n如出现应用无反应等提示是正常现象\n无需关闭")
        timeOfProcess=process_words_withDef(infors,name,len(infors))
        messagebox.showinfo("success",f"成功导入 {name} 词汇书\n共耗时{timeOfProcess}")
        choosevocabbooks.destroy()
    def run_create_vocabList():
        choosevocabbooks = Tk()
        choosevocabbooks.title("选择要导入的单词书")
        choosevocabbooks.geometry('300x300')
        vocabbooks_list=[]
        root=''
        for root1,dirs,files in walk('内置单词书'):
            vocabbooks_list=files
            root=root1
        vocabbooks_text= Text(choosevocabbooks, height=7, width=20)
        vocabbooks_text.pack(side='top')
        num=0
        for vocabbooks_name in vocabbooks_list:
            num+=1
            vocabbooks_text.insert(tkinter.END, f"单词书{num}. {vocabbooks_name}\n")
        selector=Spinbox(choosevocabbooks,from_=1,to=len(vocabbooks_list),)
        selector.pack(anchor="center")
        instruction=Label(choosevocabbooks,text="输入单词书号码\n并点击“完成选择”按钮\n导入完成后\n可选择相应词单开始背诵")
        instruction.pack(side='bottom')
        buttom_finish=Button(choosevocabbooks,text="完成选择",command=lambda:create_vocabList(vocabbooks_list,selector,root,choosevocabbooks))
        buttom_finish.pack(side='bottom')
    run_create_vocabList()

#传书生成词单------------------------------------------------------------------------------
def process_words_pureWord(words_list,table_name,countTotal,threadNum=10):
    '''turn a book's word into the database'''
    
    from threading import Thread
    threadLIst=list()
    con = sqlite3.connect('DataForUse/ecdictWords.db')
    cur = con.cursor()
    cur.execute("SELECT name _id FROM sqlite_master WHERE type ='table';")
    table_list = cur.fetchall()
    if not table_name in table_list:
        new_words_list=[]
        sqliteConnection = sqlite3.connect('DataForUse/ecdictWords.db')
        cursor = sqliteConnection.cursor()
        global count
        count=0
    
        def looping_thread(words_list,cursor,new_words_list,threadId,threadTotal):
            global count
            for word_index in range(round(threadId*len(words_list)/threadTotal),round((threadId+1)*len(words_list)/threadTotal)):
                cursor.execute(f"Select id,word,definition,translation,bnc,frq from LowLevelWords where word='{words_list[word_index]}'")
                first_fetch=cursor.fetchall()
                if len(first_fetch)==0:
                    cursor.execute(f"Select id,word,definition,translation,bnc,frq from MiddleLevelWords where word='{words_list[word_index]}'")
                    second_fetch=cursor.fetchall()    
                    if len(second_fetch)!=0:
                        infor=second_fetch[0]
                        new_words_list.append([infor[0],infor[1],infor[2],infor[3],int(infor[4].replace("notProvided",'0')),int(infor[5]),2])
                else:
                    infor=first_fetch[0]
                    new_words_list.append([infor[0],infor[1],infor[2],infor[3],int(infor[4].replace("notProvided",'0')),int(infor[5]),1])
                count+=1
                print(f"have progressed {count*100/countTotal}%")
            
        start=time.time()
        for threadId in range(10):
            threadLIst.append(Thread(target=looping_thread(words_list,cursor,new_words_list,threadId,threadNum)))
            print(f"thread {threadId} start")
            threadLIst[threadId].start()
        end=time.time()
        print(f"total cost {start-end} second")
        sqliteConnection = sqlite3.connect('DataForUse/VocabList_database.db')
        cursor = sqliteConnection.cursor()
        table_name=sub('\(.*\)','',table_name.replace("'",""))
        print(f"the table name is {table_name}")
        try:
            cursor.execute(f"drop table {table_name}")
        except:
            pass
        cursor.execute(f"create table {table_name}(id int,word text,definition text,translation text,bnc int,frq int,correct_time int,wrong_time int,fetched_level int)")
        for words_list in new_words_list:
            print(f"{words_list} inserted to {table_name}")
            cursor.executemany(f"insert into {table_name} (id,word,definition,translation,bnc,frq,correct_time,wrong_time,fetched_level) values(?,?,?,?,?,?,?,?,?)",zip((words_list[0],),(words_list[1],),(words_list[2],),(words_list[3],),(words_list[4],),(words_list[5],),(0,),(0,),(words_list[6],)))
        sqliteConnection.commit()
        cursor.close()
        return [end-start,new_words_list]

def return_words_from_file(path):
    '''input a text/pdf file output a list of word'''
    from re import findall
    black_list = ['the', 'are', 'is', 'have', 'his', 'him', 'them', 'he', 'she', 'her', 'as', 'just', 'and',
                  'has', 'do', 'in', 'does', 'did', 'a', 'they', 'there', 'com', 'www', 'com',
                  'good', 'can', 'too', 'by', 'not', 'an', 'J', 't', 'had', 'which', 'what', 'your', 'me',
                  'with', 'who', 'were', 'about', 'like', 'than', 'll', 've', 'here',
                                                                              'little', 'how', 'get', 'cid',
                  'day', 'man', 'take', 'why', 'over', 'one', 'all', 'small', 'you', 'F']
    final = set()
    string = ""
    #如果是pdf文件
    if path.split('.')[-1].lower()=='pdf':
        import pdfplumber
        with pdfplumber.open(path) as p:
            for page_number in range(len(p.pages)):
                page = p.pages[page_number]
                data = page.extract_words()
                for i in data:
                    string += i['text'] + " "
    #如果是text文件
    elif path.split('.')[-1].lower() == 'txt':
        with open(path,'r',encoding='utf-8') as f:
            string=f.read()
    textall = findall('[a-zA-Z]+', string)
    for i in textall:
        if not i.isupper() and len(i) > 3 and len(i)<25 and i.lower() not in black_list and len(findall('[A-Z]{1}',i))<=1:
            final.add(i)
    return final
#从目录内置英文原版书获取数据，选择书导入
def choose_defaulNovel():
    def set_current_list(novel_list,novel_list_text,choosenovelPage,root):
        global current_novel
        for novel_name in novel_list:
            if str(novel_list_text.get()).split('.')[0].lower() in novel_name.lower() or str(novel_list_text.get()).lower() in novel_name.lower():
                current_novel=root+"/"+novel_name
                print(current_novel)
                wordlist=list(return_words_from_file(current_novel))
                print(wordlist)
                messagebox.showinfo("Processing"," the process could last for one minute\n软件未响应是正常现象，请耐心等待")
                inforlist=process_words_pureWord(wordlist,countTotal=len(wordlist),table_name=novel_name.replace(" ","_").split('.')[0])
                messagebox.showinfo('Success', f'已添加至词单数据库,用时{inforlist[0]}')
                choosenovelPage.destroy()
                return 0
        messagebox.showinfo('Error', '内置库未收录此书\n可以通过上传文件解决')
        choosenovelPage.destroy()
    def set_bookname(listbox1,novel_list_text):
        val = listbox1.get(listbox1.curselection())
        if len(val)!=0:
            novel_list_text.insert(0,val)
    def run_choose_novelList():
        choosenovelPage = Tk()
        choosenovelPage.title("选择要导入的书")
        choosenovelPage.geometry('300x300')
        novel_list=[]
        for root1,dirs,files in walk('内置英文原版书'):
            novel_list=files
            root=root1
        novel_list_text = Entry(choosenovelPage,width=30)
        novel_list_text.pack(side='top')
        instruction=Label(choosenovelPage,text="点击书，并点击选择书完成\n最后点击完成选择，自动为您生成词单")
        instruction.pack(side='top')
        # 创建滚动条
        s = Scrollbar(choosenovelPage)
        # 设置垂直滚动条显示的位置，使得滚动条，靠右侧；通过 fill 沿着 Y 轴填充
        s.pack(side = RIGHT,fill = Y)
        # 将 selectmode 设置为多选模式，并为Listbox控件添加滚动条
        listbox1 =Listbox(choosenovelPage,selectmode = "single",height =10,width=40, yscrollcommand = s.set)
        listbox1.pack(side='top')
        for i in novel_list:
            listbox1.insert("end",i)
        buttom_finish=Button(choosenovelPage,text="完成选择",command=lambda:set_current_list(novel_list,novel_list_text,choosenovelPage,root))
        buttom_finish.pack(side='bottom')
        buttom_showname=Button(choosenovelPage,text="选择书完成",command=lambda:set_bookname(listbox1,novel_list_text))
        buttom_showname.pack(side='bottom')
    run_choose_novelList()
#用户传入英文原版书，输入地址
def choose_ImportNovel():
    def set_current_list(novel_list_text,choosenovelPage):
        global current_novel
        current_novel=novel_list_text.get()
        current_novel_name=current_novel.split('.')[0].split('\\')[-1]
        wordlist = list(return_words_from_file(current_novel))
        print("词汇截取完成")
        process_words_pureWord(wordlist,countTotal=len(wordlist),table_name=current_novel_name,threadNum=100)
        print(current_novel)
        messagebox.showinfo('Success', '英文书路径已添加')
        choosenovelPage.destroy()
    #D:\桌面文件夹\知识\书\进度\Frankenstein .pdf
    def run_choose_novelList():
        choosenovelPage = Tk()
        choosenovelPage.title("输入要导入的书")
        choosenovelPage.geometry('300x300')
        novel_list_text = Entry(choosenovelPage,width=30)
        novel_list_text.pack(side='top')
        instruction=Label(choosenovelPage,text="输入英文书的路径\n并点击完成选择按钮\n自动为您生成词单\nTips:”也可以尝试将书直接放到\n内置英文原版书文件夹\n然后从选择内置书内添加“")
        instruction.pack(side='top')
        buttom_finish=Button(choosenovelPage,text="完成选择",command=lambda:set_current_list(novel_list_text,choosenovelPage))
        buttom_finish.pack(side='bottom')
    run_choose_novelList()


#设计主页，以及其标签
homepage=Tk()
homepage.title("word-learner homepage")
homepage.geometry('850x850')
mainmenu=Menu(homepage)
memerizing_func=Menu(mainmenu)
upload_book_func=Menu(mainmenu)
upload_wordlist_func=Menu(mainmenu,font="隶书")
mainmenu.add_cascade(label="背单词",menu=memerizing_func)
memerizing_func.add_cascade(label="选择/删除词单",font="隶书",command=lambda :choose_vocaList())
memerizing_func.add_cascade(label="开始记忆词单词汇",font="隶书",command=lambda :start_remembering())
memerizing_func.add_cascade(label="开始检测词单背诵",font="隶书",command=lambda :test_memery())
mainmenu.add_cascade(label="传原版书生成词单",menu=upload_book_func,font="隶书")
upload_book_func.add_cascade(label="上传英文原版书(.pdf/.txt)",font="隶书",command=lambda :choose_ImportNovel())
upload_book_func.add_cascade(label="选择内置书",font="隶书",command=lambda :choose_defaulNovel())
mainmenu.add_cascade(label="传单词书生成词单",menu=upload_wordlist_func)
upload_wordlist_func.add_cascade(label="选择内置单词书",command=lambda:choose_defaulVocabbook(),font="隶书")
photo = PhotoImage('"image//mainpage.png"')
photo_1=photo.subsample(1,1)
btn_1=Button(homepage,image=photo_1)
btn_1.pack(side='left')
homepage.config(menu=mainmenu)
homepage.mainloop()



#1.软件特点/实用性/能运行的准备/运行的顺序






