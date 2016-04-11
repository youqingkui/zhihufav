#!/usr/bin/env python
#coding=utf-8

import os
import boto.sqs
from boto.sqs.message import Message

queue_name = os.getenv('aws_queue_name')
sqs_conn = boto.sqs.connect_to_region(os.getenv('sqs_location'), aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
zhihufav_sqs = sqs_conn.get_queue(queue_name)