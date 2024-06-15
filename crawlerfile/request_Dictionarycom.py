import time
import requests,re,os,random,json
# from playsound import playsound


user_agent_list=[
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"]
def request_Dictionarycom(word):
        url = f'https://www.dictionary.com/browse/{word}'
        header = {
            'origin': 'https://www.dictionary.com',
            'referer': f'https://www.dictionary.com/browse/{word}',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': 'Android',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'}

        request_data = requests.get(url=url, headers=header)
        p = re.compile(r'one-click-content[\s0-9a-z\-]{12}?[a-z0-9]{9}">[^<0-9]+?<')
        p1 = re.compile(r'class="app-base".*')
        data_text = p1.findall(request_data.text)[0]
        meaninglist = ''
        # 重要截取！！
        try:
            text_refered = re.findall('href="/browse/.*?OTHER WORDS FOR', data_text)[0]
            word_refered = re.findall('>[a-z]{1,}<', text_refered)
            x = ''
            for i in word_refered:
                i = i[1:-1]
                if i == 'adverb' or i == 'noun' or i == 'adjective' or i == 'verb':
                    pass
                else:
                    x += i + ' ;'
            meaninglist += f"{1}.{x}\n"
            num = 2
        except:
            num = 1

        noneList = ['See ', 'Terms and definitions labeled  ', 'The term  ', 'See under ', '']
        meaninglist_raw = p.findall(data_text)
        for i in range(len(meaninglist_raw)):
            a = meaninglist_raw[i][40:-1].replace(':', '.')
            if a not in noneList:
                meaninglist += f"{i + num}.{a}\n"

        return meaninglist

def request_Longman(word, speak=False):
        url = f'https://www.ldoceonline.com/dictionary/{word}'
        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'uid=800f236d-d764-48bb-ae62-2b7e92860115',
            'origin': 'https://www.ldoceonline.com',
            'referer': f'https://www.ldoceonline.com/dictionary/{word}',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': 'Android',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
        }

        try:
            request_data = requests.get(url=url, headers=header).text
            orgininal_data = re.findall('<span data-src-mp3=.*', request_data)
        except:
            request_Longman(word, speak=speak)


        # 查询的例子的发音+原文
        new_meaning = []
        now_list = -1

        # 单词的英文意思（索引与一级newmeaning相同）
        wordMeaning = []
        # 更多例句：
        extra_list = []
        #
        num = 1
        for i in range(len(orgininal_data)):
            if f'Play American pronunciation of {word}' in orgininal_data[i]:
                wordm = re.sub('<.*?>', '', orgininal_data[i])[4:]
                try:
                    wordm = re.findall('.*SYN', wordm)[0][:-3]
                except:
                    pass
                wordm = re.sub('[0-9]', '\n', wordm)
                wordm = re.sub('.*[A-Z]{2,}', '', wordm).replace('→', '')
                # wordm = re.sub('[\s]{2,}', ' ', wordm)
                wordMeaning.append(
                    f'------------the {num}th meaning of {word}--------------------:\nMeaning{num}:{wordm}')
                time.sleep(2)
                num += 1
                now_list += 1
                new_meaning.append(list())
            if 'Play Example' in orgininal_data[i]:
                example_pronounce = re.findall('https://.*?"', orgininal_data[i])[0][:-1]
                new_meaning[now_list].append([example_pronounce, orgininal_data[i]])
        for i in new_meaning:
            for j in i:
                j[1] = re.sub('<.*?>', '', j[1])
                if f'Examples from the Corpus{word}•' in j[1]:
                    extra_list += re.findall(f'Examples from the Corpus{word}•.*', j[1])[0][30:].split('•')
                    j[1] = re.findall(f'.*Examples from the Corpus{word}•', j[1])[0].replace(
                        f'Examples from the Corpus{word}•', '.')
                    j[1] = re.sub('[0-9→\[\]].*', '', j[1])
        num = -1
        for i in range(len(extra_list)):
            # 删除带数字的项目！！
            num += 1
            if re.findall('[0-9]', extra_list[i]) == []:
                extra_list[i] = f"Example{num}:{extra_list[i]}\n"
        if len(extra_list) == 0:
            print(
                f'sorry, the word {word} is not included by Longman....\nyou can try different forms of this word as subtittues!')
            return ''
        String = ''
        del extra_list[0]
        for i in extra_list:
            String += i
        return String

def example_sentence(word):
    try:
        session = requests.Session()
        url = f'https://skell.sketchengine.eu/api/run.cgi/concordance?query={word}&lang=English&format=json'
        header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.3.1591050086.1674259310; ske_cookieSetting_analytics=yes; ske_cookieSetting_marketing=yes; ske_cookieSettingsSaved=yes; _ga_DHRPD3K2JP=GS1.3.1674259310.1.1.1674259781.0.0.0',
    'Host': 'skell.sketchengine.eu',
    'Referer': 'https://skell.sketchengine.eu/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': random.choice(user_agent_list)
            }
        request_data = session.get(url=url, headers=header).text
        json_data=json.loads(request_data)
        example=''
        count=1
        for i in range(len(json_data['Lines'])):
            try:
                left=json_data['Lines'][i]['Left'][0]['Str']
            except:
                left=''
            try:
                middle=json_data['Lines'][i]['Kwic'][0]['Str']
            except:
                middle=''
            try:
                right=json_data['Lines'][i]['Right'][0]['Str']
            except:
                right=''           
            sentence=(left+middle+right).replace("'","''")+"\n"
            if len(sentence)!=0:
                example+=str(f"EXTRAexample{count}. {sentence}  ")
                count+=1
    except:
        print("reloading")
        example_sentence(word)
    
    return example
