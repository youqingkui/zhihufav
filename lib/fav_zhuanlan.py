#!/usr/bin/env python
#coding=utf-8

import requests
import os
import binascii
from Evernote import EvernoteMethod
from bs4 import BeautifulSoup
from note_store import noteStore
from logger_fun import logger

class Fav():
    def __init__(self, url, parent_note, receipt_handle):

        self.url = url
        self.parent_note = parent_note
        self.dev_token = os.environ.get('DeveloperToken')
        # self.noteStore = EvernoteMethod.getNoteStore(self.dev_token)
        self.noteStore = noteStore
        self.receipt_handle = receipt_handle
        self.headers = {'User-Agent':'osee2unifiedRelease/332 CFNetwork/711.3.18 Darwin/14.0.0',
           'Authorization':os.environ.get('Authorization'),
           'Content-Type':'application/json'}



    def get_content(self):
        logger.info("get_content url %s" % self.url)
        r = requests.get(self.url, headers=self.headers)
        logger.info("get_content res %s " % r.text)
        res_json = r.json()
        content = res_json.get('content', '')
        soup = BeautifulSoup(content, "html5lib")
        soup.find_all(self.remove_attrs)
        soup.html.unwrap()
        soup.head.unwrap()
        soup.body.unwrap()

        title = res_json.get('title', '')
        # question_id = res_json.get('question', {}).get('id', '')
        id    = res_json.get('id', '')
        note_url = 'https://zhuanlan.zhihu.com/p/%s' % (id)
        res = self.change_img(soup)
        title_list = title.split('\n')
        title = ''
        for t in title_list:
            title += t
        # remove \b
        title = title.replace('\b', '')
        logger.info("note_url %s" % note_url)
        logger.info("title %s" % title)
        html_content = str(soup)
        res = EvernoteMethod.makeNote(self.noteStore, title.encode('utf8'),
                                html_content, note_url, res, self.parent_note)

    def remove_attrs(self, tag):
        attrs = tag.attrs
        for k, v in attrs.items():
            if k not in ['src', 'href']:
                del tag.attrs[k]

    def change_img(self, soup):
        img_tags = soup.find_all("img")
        img_arr = [img.attrs['src'] for img in img_tags if img['src']]
        resources = EvernoteMethod.getRemoteRes(img_arr)
        index = 0
        for img in img_tags:
            if img['src']:
                hexhash = binascii.hexlify(resources[index].data.bodyHash)
                new_tag = soup.new_tag('en-media')
                new_tag['type'] = resources[index].mime
                new_tag['hash'] = hexhash
                img.replace_with(new_tag)
                index += 1
        return resources
