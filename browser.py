import os
import sys
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore
# write your code here


class Browser:

    def __init__(self):
        self.dir_name = None
        self.file_name = None
        self.path = None
        self.history_stack = deque()
        self.https = 'https://'
        self.tags_list = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']

    def set_dir(self):
        args = sys.argv
        self.dir_name = args[1]
        self.path = self.dir_name + '\\'
        if not os.path.exists(self.path):
            os.mkdir(self.dir_name)
        self.show_articles()

    def show_articles(self):
        while True:
            website_name = input()
            first_string = website_name.split('.')[0]

            if website_name != 'back':
                self.history_stack.append(first_string)

            if '.' in website_name and len(website_name.split('.')) >= 2:
                if first_string in os.listdir(self.path):
                    self.print_content(first_string)
                    continue
                else:
                    try:
                        req = requests.get(self.https + website_name)
                    except requests.exceptions.ConnectionError:
                        print('Incorrect URL')
                        continue
                    soup = BeautifulSoup(req.content, 'html.parser')
                    text_tags = ''
                    for tag in self.tags_list:
                        for line in soup.find_all(tag):
                            if line.a:
                                text_tags += Fore.BLUE + line.a.text
                                text_tags += Fore.WHITE + line.text.replace('\n', ' ').replace(line.a.text, '') + '\n'
                            else:
                                text_tags += Fore.WHITE + line.text.replace('\n', ' ') + '\n'
                    self.save_and_show(text_tags, first_string)
                    continue
            elif website_name == 'exit':
                return None
            elif website_name == 'back':
                self.history_stack.pop()
                self.turn_back()
            else:
                print('Error: Incorrect URL!')
                continue

    def turn_back(self):
        if len(self.history_stack) == 0:
            return None
        else:
            filename = self.history_stack.pop()
            self.history_stack.append(filename)
            self.print_content(filename)

    def print_content(self, filename):
        self.file_name = self.path + filename
        with open(self.file_name, 'r') as file:
            print(file.read())
            file.close()

    def save_and_show(self, page_content, page_name):
        print(page_content)
        self.file_name = self.path + page_name
        with open(self.file_name, 'w') as file:
            text = [line + '\n' for line in page_content.split('\n')]
            file.writelines(text)
            file.close()


test = Browser()
test.set_dir()
