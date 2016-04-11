#!/usr/bin/env python
#coding=utf-8
import os
from sqlalchemy import create_engine, or_, and_, not_, distinct
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, String, Float,MetaData, ForeignKey, Text

DB_CONNECT_STRING = os.getenv('zhihufav_db')

Base        = declarative_base()
engine      = create_engine(DB_CONNECT_STRING, echo=False)
DB_Session  = sessionmaker(bind=engine, autoflush=False)
session = DB_Session()
session._model_changes = {}


class CollectionQueue(Base):
    __tablename__ = 'collection_queue'

    cq_id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, default=None)
    api_url = Column(String(256), default='')
    web_url = Column(String(256), default='')
    title = Column(String(256), default='')
    is_collected = Column(Integer, default=0)
    add_time = Column(Integer, default=0)
    collected_time = Column(Integer, default=0)

    def __str__(self):
        return "CollectionQueue => { \
            cq_id:%d, answer_id:%d, api_url:'%s', web_url:'%s', title:'%s',  \
            is_collected:%d, add_time:%d, collected_time:%d}" % (
            self.cq_id, self.answer_id, self.api_url, self.web_url, self.title,
            self.is_collected, self.add_time, self.collected_time)

    __repr__ = __str__


class FavList(Base):
    __tablename__ = 'fav_list'

    id = Column(Integer, primary_key=True)
    fav_id = Column(Integer, default=None)
    api_url = Column(String(256), default='')
    web_url = Column(String(256), default='')
    title = Column(String(256), default='')
    note_book = Column(String(64), default='')

    def __str__(self):
        return "FavList => { \
            id:%d, fav_id:%d, api_url:'%s', web_url:'%s', title:'%s',  \
            note_book:'%s'}" % (
            self.id, self.fav_id, self.api_url, self.web_url, self.title,
            self.note_book)

    __repr__ = __str__


def add_fav(fav_id, note_book, title=''):
    fl = FavList()
    fl.fav_id = fav_id
    fl.api_url = 'https://api.zhihu.com/collections/%s/answers' % fav_id
    fl.web_url = 'https://www.zhihu.com/collection/%s' % fav_id
    fl.note_book = note_book
    fl.title = title
    session.add(fl)
    session.commit()
    session.close()
    print "add ok fav_id:%s, note_book:%s, title:%s" % (fav_id, note_book, title)



if __name__ == '__main__':
    print session.close()
    print session