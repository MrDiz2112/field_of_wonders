#!/home/mrdiz/anaconda3/bin/python
# -*- coding: utf-8 -*-

import re
import urllib.request

try:
    url = 'http://www.imho24.ru/answers/hobbies/detail/914/'

    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    respData = respData.decode('cp1251')

    questions = re.findall(r'В\.: (.*)<br />', str(respData))
    answers = re.findall(r'О\.: (.*)<br />', str(respData))

    for i, ans in enumerate(answers):
        answers[i] = answers[i].lower()

    saveFile = open('123.txt', 'w')

    for i in zip(answers, questions):
        line = '|'.join(i)
        saveFile.write(line+"\n")

    saveFile.close()
except Exception as e:
    print(str(e))