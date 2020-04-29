# -*- coding: utf-8 -*-
import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def db_connect():
    hostname = os.environ.get('POSTGRESQL_HOSTNAME')
    username = os.environ.get('POSTGRESQL_USERNAME')
    password = os.environ.get('POSTGRESQL_PASSWORD')
    database = os.environ.get('POSTGRESQL_DATABASE')

    return create_engine('postgres://%s:%s@%s:5432/%s' % (username, password, hostname, database))


def create_table():
    engine = db_connect()
    Base.metadata.create_all(engine)


class PageModel(Base):
    __tablename__ = "pages"

    id = Column(String(255), primary_key=True)
    link = Column('link', Text)
    store = Column('store', Text)
    scraped_at = Column('scraped_at', DateTime, default=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))


class ImageModel(Base):
    __tablename__ = "images"

    id = Column(String(255), primary_key=True)  # md5 checksum
    link = Column('link', Text)
    store = Column('store', Text)
    scraped_at = Column('scraped_at', DateTime, default=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))


class RelationModel(Base):
    __tablename__ = "page_image"

    id = Column(Integer, primary_key=True)
    page_id = Column('page_id', String(255))
    image_id = Column('image_id', String(255))
