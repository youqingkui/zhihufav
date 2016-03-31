#!/usr/bin/env python
#coding=utf-8

from lib.get_fav_list import CheckList

if __name__ == '__main__':
    # c = CheckList('https://api.zhihu.com/collections/29469118/answers', '735b3e76-e7f5-462c-84d0-bb1109bcd7dd', 10)
    # c = CheckList('https://api.zhihu.com/collections/20094118/answers', '0bf179b6-f351-4448-8421-c258f331825a', force=True)
    c = CheckList('https://api.zhihu.com/collections/20171047/answers', '16e4228e-88ef-4cca-9968-891481cf11c9', force=True)
    c.get_list()