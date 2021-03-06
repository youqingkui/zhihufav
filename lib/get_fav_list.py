#!/usr/bin/env python
# coding=utf-8

import requests, time, json, os
from boto.sqs.message import Message
from sqs import zhihufav_sqs
from db_conn import session, CollectionQueue
from instapush_notify import InstaPushNotify


s = requests.session()

class CheckList():
    def __init__(self, fav_url, parent_note, fav_id='', check_page=1, title='', force=False):
        self.check_page = check_page
        self.force = force
        self.headers = {
            'User-Agent': 'osee2unifiedRelease/332 CFNetwork/711.3.18 Darwin/14.0.0',
            'Authorization': os.environ.get('Authorization'),
            'Content-Type': 'application/json',
        }
        self.fav_url = fav_url
        self.title = title
        self.parent_note = parent_note
        self.check_num = 0
        self.fav_id = fav_id



    def get_list(self):
        r = s.get(self.fav_url, headers=self.headers)
        # print r.content
        # print r.headers
        # print r.url
        # print r.status_code
        res_json = r.json()
        paging = res_json.get('paging', {})
        next_url = paging.get('next', '')
        data_list = res_json.get('data', [])

        for answer in data_list:
            question = answer.get('question', {})
            title = question.get('title', '')
            id = int(answer.get('id', ''))
            url = answer.get('url', '')
            if title and id > 0 and url:
                find_queue = session.query(CollectionQueue).filter(CollectionQueue.answer_id == id).first()
                if not find_queue:
                    self.check_num += 1
                    web_url = 'http://www.zhihu.com/question/20070065/answer/%s' % id
                    cq = CollectionQueue()
                    cq.fav_id = self.fav_id
                    cq.title = title
                    cq.api_url = url
                    cq.web_url = web_url
                    cq.answer_id = id
                    cq.add_time = int(time.time())
                    session.add(cq)
                    session.commit()
                    session.close()

                    sqs_body = {
                        'api_url':url,
                        'parent_note':self.parent_note,
                        'answer_id':cq.answer_id
                    }
                    m = Message()
                    m.set_body(json.dumps(sqs_body))
                    zhihufav_sqs.write(m)

                else:
                    if find_queue.fav_id == 0:
                        find_queue.fav_id = self.fav_id
                        session.commit()
                    print("[Find Queue] %s" % url)


        if len(data_list):
            self.check_page = self.check_page - 1
            self.fav_url = next_url
            if self.force:
                print("force next url %s" % next_url)
                return self.get_list()

            elif self.check_page > 0:
                print("start next url %s" % next_url)
                return self.get_list()


        title = self.title
        num = self.check_num
        if num > 0:
            InstaPushNotify.notify(title, str(num))


if __name__ == '__main__':
    c = CheckList('https://api.zhihu.com/collections/29469118/answers', '735b3e76-e7f5-462c-84d0-bb1109bcd7dd', 10)
    c.get_list()




