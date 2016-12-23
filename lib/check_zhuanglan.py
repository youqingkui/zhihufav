#!/usr/bin/env python
#coding=utf-8

import requests
import redis
import os
import random
from instapush_notify import InstaPushNotify
from fav_zhuanlan import Fav
from logger_fun import logger

s = requests.session()
redis_obj = redis.Redis(host='localhost', port=6379, db=0)

class CheckZhuanLanFav(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'osee2unifiedRelease/332 CFNetwork/711.3.18 Darwin/14.0.0',
            'Authorization': os.environ.get('Authorization'),
            'Content-Type': 'application/json',
            'x-api-version': "3.0.42",
            'accept-language': "zh-Hans-CN;q=1, en-US;q=0.9",
            'accept': "*/*",
            'accept-encoding': "gzip, deflate"
        }
        self.force_check = True if random.randint(0, 9) > 7 else False

    def get_list(self, url):
        r = s.get(url, headers=self.headers)
        res_json = r.json()
        data_info = res_json.get('data', [])
        next_url = None
        if data_info and self.force_check:
            paging_dict = res_json.get('paging', {})
            next_url = paging_dict.get('next', None)
        for data in data_info:
            type_info = data.get('type', '')
            if type_info == 'article':
                data_url = data.get('url')
                data_id = (data.get('id'))
                data_title = data.get('title')
                if not data_url or not data_id or not data_title:
                    logger.error("%s error" % data)
                    continue
                if redis_obj.sismember('zhihu_zhuanlan_id', data_id):
                    logger.warning("%s %s %s exits" % (data_url, data_id, data_title))
                    continue
                logger.info("+++++++++++++++++++++++++++++++++++++++++++")
                logger.info(data_url)
                logger.info(data_id)
                logger.info(data_title)
                self.push_fav(data)
                logger.info("+++++++++++++++++++++++++++++++++++++++++++")
                logger.info("\n")
                # return

        if next_url:
            logger.info("next url %s" % next_url)
            self.get_list(next_url)

    def push_fav(self, dict_info):
        url = dict_info.get('url', '')
        data_id = dict_info.get('id')
        title = dict_info.get('title')
        # f = Fav(url, '735b3e76-e7f5-462c-84d0-bb1109bcd7dd', '')
        f = Fav(url, 'f082258a-fd9a-4713-98a0-d85fa838f019', '')
        f.get_content()
        redis_obj.sadd('zhihu_zhuanlan_id', data_id)
        InstaPushNotify.notify(title, type_info=2)

if __name__ == '__main__':
    try:
        czlf = CheckZhuanLanFav('https://api.zhihu.com/collections/29469118/contents?excerpt_len=75')
        czlf.get_list(czlf.url)
    except Exception, e:
        logger.error(Exception)
        logger.error(e)
        InstaPushNotify("error", type_info=2)



