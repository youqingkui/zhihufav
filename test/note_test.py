#!/usr/bin/env python
#coding=utf-8


from lib.tasks import add_note

# @app.task
# def add_note(url):
#     fav_note = Fav(url)
#     fav_note.get_content()

if __name__=="__main__":

    add_note.delay('https://api.zhihu.com/answers/83464968')
# fav = Fav('https://api.zhihu.com/answers/83464968')
# fav.get_content()

