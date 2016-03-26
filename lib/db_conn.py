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
DB_Session  = sessionmaker(bind=engine)
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