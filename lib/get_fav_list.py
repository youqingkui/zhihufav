#!/usr/bin/env python
# coding=utf-8

import requests, time, json
from boto.sqs.message import Message
from sqs import zhihufav_sqs
from db_conn import session, CollectionQueue




class CheckList():
    def __init__(self, check_num, fav_url):
        self.check_num = check_num
        self.headers = {
            'User-Agent': 'osee2unifiedRelease/332 CFNetwork/711.3.18 Darwin/14.0.0',
            'Authorization': 'oauth 5774b305d2ae4469a2c9258956ea49',
            'Content-Type': 'application/json',
        }
        self.fav_url = fav_url



    def get_list(self):
        r = requests.get(self.fav_url, headers=self.headers)
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
                    web_url = 'http://www.zhihu.com/question/20070065/answer/%s' % id
                    cq = CollectionQueue()
                    cq.title = title
                    cq.api_url = url
                    cq.web_url = web_url
                    cq.answer_id = id
                    cq.add_time = int(time.time())
                    session.add(cq)
                    session.commit()

                    sqs_body = {
                        'api_url':url
                    }
                    m = Message()
                    m.set_body(json.dumps(sqs_body))
                    zhihufav_sqs.write(m)

                else:
                    print("[Find Queue] %s" % url)






c = CheckList(10, 'https://api.zhihu.com/collections/29469118/answers')
c.get_list()




