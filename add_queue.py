#!/usr/bin/env python
#coding=utf-8

from lib.get_fav_list import CheckList

if __name__ == '__main__':
    c = CheckList(10, 'https://api.zhihu.com/collections/29469118/answers', '735b3e76-e7f5-462c-84d0-bb1109bcd7dd')
    c.get_list()