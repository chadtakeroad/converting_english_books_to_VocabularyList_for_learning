import requests,re
class YouDao_search:
    def __init__(self):
        self.headers = {'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN, zh;q=0.8',
               'Upgrade-Insecure-Requests': '1',
               'Host': 'dict.youdao.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                               Chrome/48.0.2564.116 Safari/537.36'
               }
    def YouDao_search_example_phrase(self,word):
        try:
            url = f'https://dict.youdao.com/result?word={word}&lang=en'
            respon = requests.get(url, headers=self.headers)
            example_phrase = list()
            example_phrase_chi = list()
            pa1 = re.compile(r'短语.*</a><p class="sen-phrase">.*?[<]{1}')
            try:
                text1 = pa1.findall(respon.text)[0]
                p1 = re.compile(r'data-v-[0-9A-Za-z]{8}>.*?</a><p class="sen-phrase">')
                for i in p1.findall(text1):
                    example_phrase.append(i[16:][:-26])
                p3 = re.compile(r'class="sen-phrase">.+?<')
                for i in p3.findall(text1):
                    example_phrase_chi.append(i[19:][:-1])
            except:
                pass
            a = ''
            for i in range(len(example_phrase)):
                a += (example_phrase[i] + ' 中文意思（网络释义仅供参考）：')
                try:
                    a += example_phrase_chi[i]
                except:
                    a += 'None'
                a += ';'
            return a
        except:
            self.YouDao_search_example_phrase(word)



    def YouDao_search_example_sentences(self,word):
        try:
            url = f'https://dict.youdao.com/result?word={word}&lang=en'
            respon = requests.get(url, headers=self.headers)
            example_sentences = list()
            try:
                pa2 = re.compile(r'[双语权威]例句.*。')
                text2 = pa2.findall(respon.text)[0]

                p2 = re.compile(r'"sen-eng" data-v-[0-9A-Za-z]{8}.+?<b>.+?</b>.+?</div><div')
                for i in p2.findall(text2):
                    new_word = i[26:][:-10].replace('</b>', '')
                    new_new_word = new_word.replace('<b>', '')
                    example_sentences.append(new_new_word)
            except:
                pass
            a = ''
            for i in example_sentences:
                a += '\n'
                a += i

            return a
        except:
            self.YouDao_search_example_sentences(word)

