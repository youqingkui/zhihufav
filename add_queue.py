#!/usr/bin/env python
#coding=utf-8

from lib.get_fav_list import CheckList
from lib.db_conn import FavList, session
import random
if __name__ == '__main__':

    fav_list = session.query(FavList).all()
    for fav in fav_list:
        print(fav.api_url)
        check_num = int(random.random() * 10 + 1)
        c = CheckList(fav.api_url, fav.note_book, fav_id=fav.id, title=fav.title, force=True)
        c.get_list()
    session.close()