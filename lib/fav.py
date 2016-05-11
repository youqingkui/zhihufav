#!/usr/bin/env python
#coding=utf-8

import requests
import os
import hashlib
import binascii
import time

from Evernote import EvernoteMethod
import evernote.edam.type.ttypes as Types
from bs4 import BeautifulSoup
from db_conn import CollectionQueue, create_session
from sqs import zhihufav_sqs, sqs_conn
from note_store import noteStore

class Fav():
    def __init__(self, url, parent_note, receipt_handle):

        self.url = url
        self.parent_note = parent_note
        self.dev_token = os.environ.get('DeveloperToken')
        # self.noteStore = EvernoteMethod.getNoteStore(self.dev_token)
        self.noteStore = noteStore
        self.receipt_handle = receipt_handle
        self.headers = {'User-Agent':'osee2unifiedRelease/332 CFNetwork/711.3.18 Darwin/14.0.0',
           'Authorization':'oauth 5774b305d2ae4469a2c9258956ea49',
           'Content-Type':'application/json'}



    def get_content(self):
        r = requests.get(self.url, headers=self.headers)
        print self.url
        print r.text
        res_json = r.json()
        content = res_json.get('content', '')
        soup = BeautifulSoup(content, "html5lib")
        soup.find_all(self.remove_attrs)
        soup.html.unwrap()
        soup.head.unwrap()
        soup.body.unwrap()

        title = res_json.get('question', {}).get('title', '')
        question_id = res_json.get('question', {}).get('id', '')
        id    = res_json.get('id', '')
        note_url = 'http://www.zhihu.com/question/%s/answer/%s' % (question_id, id)
        res = self.change_img(soup)
        title_list = title.split('\n')
        title = ''
        for t in title_list:
            title += t
        print("note_url %s" % note_url)
        print("title %s" % title)
        html_content = str(soup)
        EvernoteMethod.makeNote(self.noteStore, title.encode('utf8'), html_content, note_url, res, self.parent_note)

        session = create_session()
        find_queue = session.query(CollectionQueue).filter(CollectionQueue.api_url == self.url).first()
        if find_queue:
            find_queue.is_collected = 1
            find_queue.collected_time = int(time.time())
            session.commit()

            sqs_conn.delete_message_from_handle(zhihufav_sqs, self.receipt_handle)

        session.close()




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
