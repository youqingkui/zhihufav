#!/usr/bin/env python
#coding=utf-8
import os
from evernote.api.client import EvernoteClient

token = os.environ.get('DeveloperToken')
client = EvernoteClient(token=token, sandbox=False)
client.service_host = 'app.yinxiang.com'
noteStore = client.get_note_store()