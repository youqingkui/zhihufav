#!/usr/bin/env python
#coding=utf-8

import requests
import os
import hashlib
from lib.Evernote import EvernoteMethod
import evernote.edam.type.ttypes as Types
from bs4 import BeautifulSoup

import HTMLParser
h = HTMLParser.HTMLParser()

dev_token = os.environ.get('DeveloperToken')
noteStore = EvernoteMethod.getNoteStore(dev_token)

headers = {'User-Agent':'osee2unifiedRelease/332 CFNetwork/711.3.18 Darwin/14.0.0',
           'Authorization':'oauth 5774b305d2ae4469a2c9258956ea49',
           'Content-Type':'application/json'}



url = 'https://api.zhihu.com/answers/83350780'

r = requests.get(url, headers=headers)
res_json = r.json()
content = res_json.get('content', '')
soup = BeautifulSoup(content, "html5lib")
# soup = BeautifulSoup(content)

def remove_attrs(tag):
    attrs = tag.attrs
    for k, v in attrs.items():
        if k not in ['src', 'href']:
            del tag.attrs[k]

soup.find_all(remove_attrs)

soup.html.unwrap()
soup.head.unwrap()
soup.body.unwrap()

print(str(soup))

html_content = str(soup)
EvernoteMethod.makeNote(noteStore, 'hi', html_content)