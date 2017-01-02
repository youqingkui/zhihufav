#!/usr/bin/env python
#coding=utf-8

import logging
import time

def get_logger():
    logger = logging.getLogger("threading_example")
    logger.setLevel(logging.INFO)
    date_info = time.strftime('%Y-%m-%d')
    fh = logging.FileHandler("/data/www/logs/zhuanlan.log.%s" % date_info)
    # fh = logging.FileHandler("/Users/youqingkui/PycharmProjects/zhihufav/zhuanlan.log.%s" % date_info)
    fmt = '%(asctime)s|%(threadName)s|%(levelname)s| %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = get_logger()

if __name__ == '__main__':
    logger.debug("hello debug")
    logger.warning("hello warning")
    logger.info("hello info")
    logger.error("hello error")