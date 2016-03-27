#!/usr/bin/env python
#coding=utf-8

import json
from lib.sqs import zhihufav_sqs
from lib.tasks import add_note


if __name__=="__main__":
    sqs_info = zhihufav_sqs.get_messages(10)
    for sqs in sqs_info:
        sqs_body = sqs.get_body()
        receipt_handle = sqs.receipt_handle
        sqs_json = json.loads(sqs_body)
        api_url = sqs_json.get('api_url')
        parent_note = sqs_json.get('parent_note')
        add_note.delay(api_url, parent_note, receipt_handle)

