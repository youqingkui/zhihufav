#!/usr/bin/env python
#coding=utf-8
from __future__ import absolute_import

from lib.tasks import app, add, add_note

# @app.task
# def add_note(url):
#     fav_note = Fav(url)
#     fav_note.get_content()

if __name__=="__main__":

    add_note.delay('https://api.zhihu.com/answers/83464968')