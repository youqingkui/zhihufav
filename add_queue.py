#!/usr/bin/env python
#coding=utf-8

from lib.get_fav_list import CheckList

if __name__ == '__main__':
    # c = CheckList('https://api.zhihu.com/collections/29469118/answers', '735b3e76-e7f5-462c-84d0-bb1109bcd7dd', 10)
    c = CheckList('https://api.zhihu.com/collections/20094118/answers', '0bf179b6-f351-4448-8421-c258f331825a', force=True)
    c.get_list()