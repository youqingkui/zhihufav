#!/usr/bin/env python
#coding=utf-8

import os
from instapush import Instapush, App

class InstaPushNotify():



    @staticmethod
    def notify(title, check_num):
        app = App(appid=os.getenv('instapush_id'), secret=os.getenv('instapush_secret'))
        try:
            res = app.notify(event_name='get_list', trackers={'title': title, 'check_num':check_num})
            print res
        except Exception, e:
            print Exception
            print e




if __name__ == '__main__':
    InstaPushNotify.notify('收藏', 1)