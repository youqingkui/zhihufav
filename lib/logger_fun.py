#!/usr/bin/env python
#coding=utf-8

import logging
import time

def get_logger():
    logger = logging.getLogger("threading_example")
    logger.setLevel(logging.DEBUG)
    date_info = time.strftime('%Y-%m-%d')
    # fh = logging.FileHandler("/data/www/logs/zhuanlan.log.%s" % date_info)
    fh = logging.FileHandler("/Users/youqingkui/PycharmProjects/zhihufav/zhuanlan.log.%s" % date_info)
    fmt = '%(asctime)s|%(threadName)s|%(levelname)s| %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


logger = get_logger()