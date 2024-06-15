#  English Books Foreteller
项目简介
环境配置：tkinter,squlite3,pdfplumber,re,requests,os,json包
一.tkinter界面学习单词：
1.项目主文件：mainpage.py（本来是多个文件分开的，但是想打包成exeutable所以和一起了）
2.项目附带文件：DataForUse目录下的两个单词database。（本项目不需要联网）
3.主要功能：
（1）上传txt/pdf的英文原版书，生成按照词频排序的词单，可保存在exported_list目录下。
（2）选择内置的英文原版txt书，或者内置的单词书，生成背诵的词单，可保存在exported_list目录下。
（3）以无中文，只有中文，正序，倒序方式浏览词单。
（4）以无中文，中英结合方式测试词汇掌握程度。
4.重点功能的实现：
（1）读取，统计词频（运用技术：正则匹配和高频词去除）：利用pdfplumber的api读取pdf文件，然后，介于英文语言断词和短句的优越性，利用正则匹配单一大写字母且剩下小写字母或者全部小写字母的单词。后期为了筛选出常用词汇，利用10多本书的单词，按照词频排序，生成一个高词频的词单。这些词单中大多数将不会被匹配，比如冠词，不定式等等。
（2）传入文件，生成词单（数据库二叉搜索和多线程）：生成要查找的词后，利用squlite3数据库默认的二叉搜索和threading的多线程，分别在高频词汇库（大约13000个词，内含词频）和中频词汇库（34万个词）进行一一查找。查找完成后在数据库内生成表格，存储收集的信息，以便背诵使用。
二.学习词单脚本（补充项目一的第四功能，并且有更成熟的单词检测系统）：
1.项目主文件：test_memery.py
2.项目附带文件：DataForUse目录下的自动生成的test_memery.db。（本项目需要联网）
3.主要功能：
（1）读取txt文件（格式为一行一个单词形式，或者WORD：xxxx形式），生成
关于一个英文单词的至少有35个英文例句，更多词意等的txt文档供学习，在主程序控制台以
英文词义检测掌握程度，设置正确次数大于错误次数2值后不再复习
（后期准备通过遗忘曲线控制熟练度）
（2）可以通过项目一的只有单词模式导出的txt文件直接生成，但是可能需要比较长时间
4.	重点功能的实现
（1）逐个爬取单词信息：利用requests库的session进行多次连续爬取：先按照词汇查询网页网址规律找到目标单词的网页，在网页源代码中有时候直接导成json直接拼接或者利用正则匹配匹配特定的tag如<audio>.*?<audio/>
（2）爬取成功后保存到txt文档储存。
![image](https://github.com/chadtakeroad/converting_english_books_to_VocabularyList_for_learning/assets/119279064/84933f4d-1949-4e68-a966-146dab7c26a9)
![image](https://github.com/chadtakeroad/converting_english_books_to_VocabularyList_for_learning/assets/119279064/621d2dad-a3d8-4d60-8e95-88ac9b10fd86)
