#!/usr/bin/env python
#coding=utf-8

from lib.get_fav_list import CheckList
from lib.db_conn import FavList, session
import random
if __name__ == '__main__':

    fav_list = session.query(FavList).all()
    for fav in fav_list:
        print fav.api_url
        check_num = int(random.random() * 10 + 1)
        c = CheckList(fav.api_url, fav.note_book, title=fav.title, force=True)
        # c = CheckList('https://api.zhihu.com/collections/20094118/answers', '0bf179b6-f351-4448-8421-c258f331825a', force=True)
        # c = CheckList('https://api.zhihu.com/collections/20171047/answers', '16e4228e-88ef-4cca-9968-891481cf11c9', force=True)

        # 有图真像
        # c = CheckList('https://api.zhihu.com/collections/26347524/answers', '5bf8f6d7-e007-4f56-8424-a8c485d4ebeb', force=True)
        c.get_list()

    session.close()