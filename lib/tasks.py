#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import


from lib.celery_app import app
from lib.fav import Fav

@app.task
def add(x, y):
    return x + y


@app.task
def add_note(url, parent_note, receipt_handle):
    fav_note = Fav(url, parent_note, receipt_handle)
    fav_note.get_content()