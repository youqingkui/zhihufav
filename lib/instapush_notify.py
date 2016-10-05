#!/usr/bin/env python
#coding=utf-8

import os
import time
from instapush import Instapush, App

class InstaPushNotify():



    @staticmethod
    def notify(title, check_num=0, type_info=1):
        app = App(appid=os.getenv('instapush_id'), secret=os.getenv('instapush_secret'))
        try:
            if type_info == 1:
                res = app.notify(event_name='get_list', trackers={'title': title, 'check_num':check_num})
            else:
                date_info = time.strftime('%Y-%m-%d %H:%M:%S')
                res = app.notify(event_name='zhihufav', trackers={'title': title, 'date':date_info})
            print(res)
        except Exception, e:
            print(Exception)
            print(e)




if __name__ == '__main__':
    InstaPushNotify.notify('收藏', type_info=2)