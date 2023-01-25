##TO DO:
# add more thread so that it could process faster
# seperate the big study vocabulary list into smaller one and sign on days for it to be remembered
# adding more example sentences!
#————————————————————————————————————————————————————————————————————————————————————————————————————————————
import tkinter
from tkinter import *
from random import choice
import sqlite3
from re import findall,sub
from tkinter import *
from tkinter import messagebox
import os
import pdfplumber
current_novel=''
current_vocablist=''
#btn_1
#背单词功能----------------------------------------------------------------------------------
def choose_vocaList():
    def set_current_list(table_list,selector,chooseVocabPage):
        global current_vocablist
        current_vocablist = table_list[int(selector.get()) - 1][0]
        print(current_vocablist)
        chooseVocabPage.destroy()
    def delete_vocablist(table_list,selector,chooseVocabPage):
        con = sqlite3.connect('DataForUse/VocabList_database.db')
        cur = con.cursor()
        #select * from sqlite_master where type='table'
        cur.execute(f"Drop table {table_list[int(selector.get())-1][0]}")
        con.commit()
        cur.close()
        messagebox.showinfo("success!",f"successfully delete table {table_list[int(selector.get())-1][0]}")
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
        table_list_text = Text(chooseVocabPage, height=6, width=20,font='RockwellExtraBold')
        table_list_text.pack(side='top')
        table_num=0
        for table_name in table_list:
            table_num+=1
            table_list_text.insert(tkinter.END, f"词单{table_num}. {table_name[0]}\n")
        selector=Spinbox(chooseVocabPage,from_=0,to=len(table_list),font='RockwellExtraBold',)
        selector.pack(anchor="center")
        instruction=Label(chooseVocabPage,text="输入词单号码\n并点击完成选择按钮选择当前背诵词单\n再次点击背单词下选项\n开始记忆/背诵单词",fg="blue",font='RockwellExtraBold')
        instruction.pack(anchor='e')
        buttom_finish=Button(chooseVocabPage,text="完成选择",fg="blue",command=lambda:set_current_list(table_list,selector,chooseVocabPage))
        buttom_finish.pack(side='bottom')
        buttom_delete=Button(chooseVocabPage,text="删除词单",fg="blue",command=lambda:delete_vocablist(table_list,selector,chooseVocabPage))
        buttom_delete.pack(side="bottom")

    run_choose_vocaList()
def start_remembering():
    homepage_1 = Tk()
    homepage_1.title("Study vocabulary!")
    homepage_1.geometry('850x800')
    def mark_important_word(Notice,text_input):
        Notice.config(text=text_input.get())
    def run_start_remembering(homepage_1):
        def retore_desktop(homepage_1):
            homepage_1.destroy()
        global current_vocablist
        text_input=Entry(homepage,width=10)
        text_input.pack(side='top')
        if len(current_vocablist)==0:
            homepage_1.destroy()
            messagebox.showwarning("warning","你还没有选择相应的词单！")
        else:
            Notice=Label(homepage_1,text="importantWordList",font=('times',20,"italic"))
            Notice.pack(side="top")
            scroll_bar = Scrollbar(homepage_1)
            scroll_bar.pack(side=RIGHT,fill=Y)
            mylist = Listbox(homepage_1,yscrollcommand=scroll_bar.set,width=20,height=30,background="Wheat",font='BahnschriftLight')
            mylist.pack(side='bottom', fill=BOTH)
            adjust=Button(homepage_1,text="mark important word",font=("BahnschriftLight",20),command=lambda:mark_important_word(Notice,text_input))
            adjust.pack(side="top")
            refresh=Button(homepage_1,text="refresh the page          ",font=("BahnschriftLight",20),command=lambda:run_start_remembering(homepage_1))
            refresh.pack(side="left")
            hide=Button(homepage_1,text="           quit            ",font=("BahnschriftLight",20),command=lambda:retore_desktop(homepage_1))
            hide.pack(side="right")
            #数据库部分
            con_1 = sqlite3.connect('DataForUse/VocabList_database.db')
            cur_1 = con_1.cursor()
            con_2 = sqlite3.connect('DataForUse/ecdictWords.db')
            cur_2 = con_2.cursor()
            cur_1.execute(f"select word,definition,translation,bnc,frq,fetch_level from {current_vocablist} order by fetch_level,frq desc")
            inforList=cur_1.fetchall()
            for infor in (inforList):
                mylist.insert(END,f"WORD:         {infor[0]}---------------------------")
                mylist.insert(END,f"definition:{infor[1]}")
                mylist.insert(END, f"translation:{infor[2]}")
                mylist.insert(END, f"The British National Corpus:\n{infor[3]}")
                mylist.insert(END, f"frequency:{infor[4]}")
                try:
                    cur_2.execute(f"select detail from LowLevelWordsExample where word={infor[0]}")
                    print("trying to add details")
                    mylist.insert(END,f"example:{cur_2.fetchone()}")
                except:
                    pass
    run_start_remembering(homepage_1)
def test_memery():
    homepage_2 = Tk()
    homepage_2.title("word-learner testingVocab")
    homepage_2.geometry('850x800')
    def run_test_memery(homepage_2):
        if len(current_vocablist) == 0:
            messagebox.showwarning("warning", "你还没有选择相应的词单！")
            homepage_2.destroy()
        else:
            #前后匹配的词组
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
                    def generate_question(mylist):
                        cur.execute(
                            f"select word,definition,translation,correct_time,wrong_time from {current_vocablist} where correct_time-wrong_time<=2")
                        testwords_list = cur.fetchall()
                        current_word_list = choice(testwords_list)
                        if current_word_list[1] == ' 1/.notProvided':
                            mylist.insert(END,str(current_word_list[2]))
                        else:
                            mylist.insert(END, str(current_word_list[1]))
                        afbf.append(current_word_list[0])
                        current_word_list_correcttime.append(current_word_list[3])
                    def generate_question_2(mylist):
                        cur.execute(
                            f"select word,definition,translation,correct_time,wrong_time from {current_vocablist} where correct_time-wrong_time<=2")
                        testwords_list = cur.fetchall()
                        current_word_list = choice(testwords_list)
                        if current_word_list[1] == ' 1/.notProvided':
                            mylist.insert(END,str(current_word_list[2]))
                        else:
                            mylist.insert(END, str(current_word_list[1]))
                            mylist.insert(END,str(current_word_list[2]))
                        afbf.append(current_word_list[0])
                        current_word_list_correcttime.append(current_word_list[3])
            scroll_bar = Scrollbar(homepage_2)
            scroll_bar.pack(side=RIGHT, fill=Y)
            mylist = Listbox(homepage_2,bd=20, yscrollcommand=scroll_bar.set, width=40, height=30, background="Wheat",font='BahnschriftLight')
            mylist.pack(side='bottom', fill=BOTH)
            input_frame_1 = Entry(homepage_2,textvariable="enter your answer here" ,font=('times',20,"italic"),width=15)
            input_frame_1.pack(side="top")
            btn_frame_1=Button(master=homepage_2,text="click to check answer entered above",font=('times',16,"italic"),command=lambda :check_question(input_frame_1))
            btn_frame_1.pack(side="top")
            btn_frame_2=Button(master=homepage_2,text="click to generate a new question EnglishONLY",font=('times',13,"italic"),command=lambda :generate_question(mylist))
            btn_frame_2.pack(side="top",)
            btn_frame_3=Button(master=homepage_2,text="click to generate a new question",font=('times',13,"italic"),command=lambda :generate_question_2(mylist))
            btn_frame_3.pack(side="top")
    run_test_memery(homepage_2)

#传单词书生成词单-----------------------------------------------------------------------------------------------
def read_vocabbooks(path, encoding='utf-8'):
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
def process_words(words_list,table_name):
    con = sqlite3.connect('DataForUse/ecdictWords.db')
    cur = con.cursor()
    cur.execute("SELECT name _id FROM sqlite_master WHERE type ='table';")
    table_list = cur.fetchall()
    if not table_name in table_list:
        new_words_list=[]
        sqliteConnection = sqlite3.connect('DataForUse/ecdictWords.db')
        cursor = sqliteConnection.cursor()
        count=0.0
        lenth_Of_word=len(words_list)
        for word in words_list:
            count+=1
            cursor.execute(f"Select id,word,definition,bnc,frq from LowLevelWords where word='{word[0]}'")
            first_fetch=cursor.fetchall()
            if len(first_fetch)==0:
                cursor.execute(f"Select id,word,definition,bnc,frq from MiddleLevelWords where word='{word[0]}'")
                second_fetch=cursor.fetchall()
                if len(second_fetch)==0:
                    continue
                else:
                    infor=second_fetch[0]
                    if len(infor)==0:
                        count-=1
                    new_words_list.append([infor[0],infor[1],infor[2],word[1],int(infor[3].replace("notProvided",'0')),int(infor[4]),2])
            else:
                infor=first_fetch[0]
                new_words_list.append([infor[0],infor[1],infor[2],word[1],int(infor[3].replace("notProvided",'0')),int(infor[4]),1])
            print(f"已经加载完{str((count/lenth_Of_word)*100)[:4]}%了！")

        sqliteConnection = sqlite3.connect('DataForUse/VocabList_database.db')
        cursor = sqliteConnection.cursor()
        table_name=sub('\(.*\)','',table_name)
        print(table_name)
        try:
            cursor.execute(f"drop table {table_name}")
        except:
            pass
        cursor.execute(f"create table {table_name}(id int,word text,definition text,translation text,bnc int,frq int,correct_time int,wrong_time int,fetch_level int)")
        for words_list in new_words_list:
            cursor.executemany(f"insert into {table_name} (id,word,definition,translation,bnc,frq,correct_time,wrong_time,fetch_level) values(?,?,?,?,?,?,?,?,?)",zip((words_list[0],),(words_list[1],),(words_list[2],),(words_list[3],),(words_list[4],),(words_list[5],),(0,),(0,),(words_list[6],)))
        sqliteConnection.commit()
        cursor.close()
def choose_defaulVocabbook():
    def create_vocabList(vocabbooks_list,selector,root,choosevocabbooks):
        name=str(vocabbooks_list[int(selector.get()) - 1]).split('.')[0]
        path = str(root)+"/"+vocabbooks_list[int(selector.get()) - 1]
        infors=read_vocabbooks(path)
        messagebox.showinfo("warning", f"本文件将加载关于{len(infors)}个单词的信息，请耐心等待\n进度较慢，稍安务躁捏")
        process_words(infors,name)
        messagebox.showinfo("success",f"成功导入 {name} 词汇书")
        choosevocabbooks.destroy()
    def run_create_vocabList():
        choosevocabbooks = Tk()
        choosevocabbooks.title("选择要导入的单词书")
        choosevocabbooks.geometry('300x300')
        vocabbooks_list=[]
        root=''
        for root1,dirs,files in os.walk('内置单词书'):
            vocabbooks_list=files
            root=root1
        vocabbooks_text= Text(choosevocabbooks, height=7, width=20,font='RockwellExtraBold')
        vocabbooks_text.pack(side='top')
        num=0
        for vocabbooks_name in vocabbooks_list:
            num+=1
            vocabbooks_text.insert(tkinter.END, f"单词书{num}. {vocabbooks_name}\n")
        selector=Spinbox(choosevocabbooks,from_=1,to=len(vocabbooks_list),font='RockwellExtraBold',)
        selector.pack(anchor="center")
        instruction=Label(choosevocabbooks,text="输入单词书号码\n并点击“完成选择”按钮\n导入完成后\n可选择相应词单开始背诵",fg="blue",font='RockwellExtraBold')
        instruction.pack(side='bottom')
        buttom_finish=Button(choosevocabbooks,text="完成选择",fg="blue",command=lambda:create_vocabList(vocabbooks_list,selector,root,choosevocabbooks))
        buttom_finish.pack(side='bottom')
    run_create_vocabList()

#传书生成词单------------------------------------------------------------------------------
def process_words_1(words_list,table_name):
    con = sqlite3.connect('DataForUse/ecdictWords.db')
    cur = con.cursor()
    cur.execute("SELECT name _id FROM sqlite_master WHERE type ='table';")
    table_list = cur.fetchall()
    if not table_name in table_list:
        new_words_list=[]
        sqliteConnection = sqlite3.connect('DataForUse/ecdictWords.db')
        cursor = sqliteConnection.cursor()
        count = 0
        length=len(words_list)
        for word in words_list:
            count+=1
            cursor.execute(f"Select id,word,definition,translation,bnc,frq from LowLevelWords where word='{word}'")
            first_fetch=cursor.fetchall()
            if len(first_fetch)==0:
                cursor.execute(f"Select id,word,definition,translation,bnc,frq from MiddleLevelWords where word='{word}'")
                second_fetch=cursor.fetchall()
                if len(second_fetch)==0:
                    count -= 1
                else:
                    infor=second_fetch[0]
                    new_words_list.append([infor[0],infor[1],infor[2],infor[3],int(infor[4].replace("notProvided",'0')),int(infor[5]),2])
            else:
                infor=first_fetch[0]
                new_words_list.append([infor[0],infor[1],infor[2],infor[3],int(infor[4].replace("notProvided",'0')),int(infor[5]),1])
            print(f"已经加载{str((count/length)*100)[:4]}%了")

        sqliteConnection = sqlite3.connect('DataForUse/VocabList_database.db')
        cursor = sqliteConnection.cursor()
        table_name=sub('\(.*\)','',table_name)
        table_name=table_name.replace('-',"_").replace(",","_")
        print(table_name)
        try:
            cursor.execute(f"drop table {table_name}")
        except:
            pass
        cursor.execute(f"create table {table_name} (id int,word text,definition text,translation text,bnc int,frq int,correct_time int,wrong_time int,fetch_level int)")
        for words_list in new_words_list:
            cursor.executemany(f"insert into {table_name} (id,word,definition,translation,bnc,frq,correct_time,wrong_time,fetch_level) values(?,?,?,?,?,?,?,?,?)",zip((words_list[0],),(words_list[1],),(words_list[2],),(words_list[3],),(words_list[4],),(words_list[5],),(0,),(0,),(words_list[6],)))
        sqliteConnection.commit()
        cursor.close()
def return_words_from_file(path):
    from re import findall
    highcase="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
        if str(novel_list_text.get())=="":
            messagebox.showwarning("warning","你好像还没输入任何东西，生气了，退回到主界面了")
            choosenovelPage.destroy()
        for novel_name in novel_list:
            if str(novel_list_text.get()).split('.')[0].lower() in novel_name.lower() or str(novel_list_text.get()).lower() in novel_name.lower():
                current_novel=root+"/"+novel_name
                print(current_novel)
                wordlist=list(return_words_from_file(current_novel))
                messagebox.showinfo("Processing"," the process could last for one minute\n软件未响应是正常现象，请耐心等待\n进度较慢，稍安务躁捏")
                process_words_1(wordlist,table_name=novel_name.replace(" ","_").split('.')[0])
                messagebox.showinfo('Success', '已添加至词单数据库')
                choosenovelPage.destroy()
                return 0
        messagebox.showinfo('Error', '内置库未收录此书\n可以通过上传文件解决')
        choosenovelPage.destroy()
    def run_choose_novelList():
        choosenovelPage = Tk()
        choosenovelPage.title("选择内置的英文原版书")
        choosenovelPage.geometry('400x400')
        novel_list=[]
        root=''
        for root1,dirs,files in os.walk('内置英文原版书'):
            novel_list=files
            root=root1
        buttom_finish=Button(choosenovelPage,text="完成选择",fg="blue",font='RockwellExtraBold',command=lambda:set_current_list(novel_list,novel_list_text,choosenovelPage,root))
        buttom_finish.pack(side='bottom')
        books_text= Text(choosenovelPage, height=13, width=60,font='RockwellExtraBold')
        books_text.pack(side='bottom')
        num=0
        for novel_name in novel_list:
            num+=1
            books_text.insert(END, f"英文书{num}. {novel_name}\n")
        novel_list_text = Entry(choosenovelPage,width=30)
        novel_list_text.pack(side='top')
        instruction=Label(choosenovelPage,text="输入要导入的书名(大小写随意)\n并点击完成选择按钮\n自动为您生成词单",fg="blue",font='RockwellExtraBold')
        instruction.pack(side='top')
    run_choose_novelList()
#用户传入英文原版书，输入地址
def choose_ImportNovel():
    def set_current_list(novel_list_text,choosenovelPage):
        global current_novel
        current_novel=novel_list_text.get()
        try:
            current_novel_name=current_novel.split('.')[0].split('\\')[-1]
            wordlist = list(return_words_from_file(current_novel))
        except:
            messagebox.showwarning("warning","传入的单词书路径有问题")
            choosenovelPage.destroy()
        messagebox.showinfo('Waiting', '英文书路径已添加\nwindows系统的小单会一直展示添加的词汇！\n进度较慢，稍安务躁捏')
        process_words_1(wordlist, table_name=current_novel_name)
        print(current_novel)
        messagebox.showinfo('Success', '词单已添加')
        choosenovelPage.destroy()
    def run_choose_novelList():
        choosenovelPage = Tk()
        choosenovelPage.title("上传英文原版书")
        choosenovelPage.geometry('300x300')
        novel_list_text = Entry(choosenovelPage,width=30)
        novel_list_text.pack(side='top')
        instruction=Label(choosenovelPage,text="输入英文书的路径\n并点击完成选择按钮\n自动为您生成词单\nTips:”也可以尝试将书直接放到\n内置英文原版书文件夹\n然后从选择内置书内添加“",fg="blue",font='RockwellExtraBold')
        instruction.pack(side='top')
        buttom_finish=Button(choosenovelPage,text="完成选择",fg="blue",font='RockwellExtraBold',command=lambda:set_current_list(novel_list_text,choosenovelPage))
        buttom_finish.pack(side='bottom')
    run_choose_novelList()


#设计主页，以及其标签
homepage=Tk()
homepage.title("word-learner homepage")
homepage.geometry('850x800')


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

photo = PhotoImage(file = "image\\wallhaven-6qlllw_1920x1080.png")
photo_1=photo.subsample(1,1)
btn_1=Button(homepage,image=photo_1)
btn_1.pack(side='left')
homepage.config(menu=mainmenu)
homepage.mainloop()