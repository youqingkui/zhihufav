#!/usr/bin/env python
#coding=utf-8

from lib.fav import Fav


fav = Fav('https://api.zhihu.com/answers/83464968')
fav.get_content()

