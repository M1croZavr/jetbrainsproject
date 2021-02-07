import requests
from bs4 import BeautifulSoup
import sys


s = requests.Session()


class Translator:

    def __init__(self):
        self.args = sys.argv
        self.languages = []
        self.lang_to_tr = None
        self.lang_from_tr = None
        self.word_to_tr = None
        self.tr_url = None
        self.req = None
        self.languages = {1: 'arabic', 2: 'german', 3: 'english', 4: 'spanish', 5: 'french', 6: 'hebrew', 7: 'japanese',
                          8: 'dutch', 9: 'polish', 10: 'portuguese', 11: 'romanian', 12: 'russian', 13: 'turkish'}

    def ask_w_and_lang(self):
        if self.args[2] == 'all':
            self.get_translations_all_lang()
        else:
            if self.args[2] not in self.languages.values():
                print(f'Sorry, the program doesn\'t support {self.args[2]}')
                return None
            tr_dir = f'{self.args[1]}-{self.args[2]}'
            self.tr_url = 'https://context.reverso.net/translation/' + tr_dir + '/' + self.args[3]
            self.get_req()

    def get_req(self):
        self.req = s.get(self.tr_url, headers={'User-Agent': 'Mozilla/5.0'})
        if self.req.status_code == 404:
            print(f'Sorry, unable to find {self.args[3]}')
            return None
        self.get_translations(self.req)

    def get_translations(self, request):
        soup = BeautifulSoup(request.content, 'html.parser')
        words_list = [line.text.replace('\n', '').strip() for line in soup.find_all(class_='translation')]
        examples_list_from = list(filter(lambda x: x != '',
                                  [line.text.replace('\n', '').strip() for line in soup.find_all('div', class_='src')]))
        examples_list_to = list(filter(lambda x: x != '',
                                [line.text.replace('\n', '').strip() for line in soup.find_all('div', class_='trg')]))
        file_list_ = [self.args[2].capitalize() + ' ' + 'Translations:']
        words_to_show = 5
        examples_to_show = 5
        if len(words_list) < words_to_show:
            words_to_show = len(words_list) - 1
            file_list_.append(words_list)
        for i in range(words_to_show):
            file_list_.append(words_list[i + 1])
        file_list_.append(' ')
        file_list_.append(self.args[2].capitalize() + ' ' + 'Examples:')
        for j in range(examples_to_show):
            file_list_.append(examples_list_from[j])
            file_list_.append(examples_list_to[j])
            file_list_.append(' ')
        with open(f'{self.args[3]}.txt', 'w', encoding='utf-8') as file:
            for line in file_list_:
                file.write(line + '\n')
        file = open(f'{self.args[3]}.txt', 'r', encoding='utf-8')
        print(file.read())
        file.close()

    def get_translations_all_lang(self):
        lang_list = [lang for lang in self.languages.values() if lang != self.args[1]]
        file_list = []
        for lan in lang_list:
            request = s.get('https://context.reverso.net/translation/' + f'{self.args[1]}-'
                            f'{lan}' + '/' + self.args[3], headers={'User-Agent': 'Mozilla/5.0'})
            if request.status_code == 404:
                print(f'Sorry, unable to find {self.args[3]}')
                return None
            elif request.status_code != 200 and request.status_code != 404:
                print('Something wrong with your internet connection')
                return None
            soup = BeautifulSoup(request.content, 'html.parser')
            words_list = [line.text.replace('\n', '').strip() for line in soup.find_all(class_='translation')]
            examples_list_from = list(filter(lambda x: x != '',
                                      [line.text.replace('\n', '').strip() for line in soup.find_all('div',
                                                                                                     class_='src')]))
            examples_list_to = list(filter(lambda x: x != '',
                                    [line.text.replace('\n', '').strip() for line in soup.find_all('div',
                                                                                                   class_='trg')]))
            if len(words_list) == 1:
                words_list.append('Not supported')

            file_list.append(lan.capitalize() + " " + 'Translations:')
            file_list.append(words_list[1])
            file_list.append(' ')
            file_list.append(lan.capitalize() + " " + 'Example:')
            file_list.append(examples_list_from[0] + ':')
            file_list.append(examples_list_to[0])
            file_list.append(' ')
            file_list.append(' ')

        with open(f'{self.args[3]}.txt', 'w', encoding='utf-8') as file_to_write:
            for line in file_list:
                file_to_write.write(line + '\n')
        with open(f'{self.args[3]}.txt', 'r', encoding='utf-8') as file_to_read:
            print(file_to_read.read())


trans = Translator()
trans.ask_w_and_lang()
