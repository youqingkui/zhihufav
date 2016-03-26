#!/usr/bin/env python
#coding=utf-8

from lib.sqs import zhihufav_sqs, sqs_conn


sqs_info = zhihufav_sqs.get_messages()
receipt_handle =  sqs_info[0].receipt_handle
print "receipt_handle:%s" % receipt_handle
a = sqs_conn.delete_message_from_handle(zhihufav_sqs,receipt_handle)
print a