# -*- coding: utf-8 -*-
import os
import sys

from server import app


SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

dev_db = 'sqlite:////' + os.path.join(os.path.dirname(app.root_path), 'data.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)

RESTFUL_JSON=dict(ensure_ascii=False)

# mariadb
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABSE = 'example'
# USERNAME = 'root'
# PASSWORD = 'password'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABSE)

# SQLALCHEMY_DATABASE_URI = DB_URI

# SQLALCHEMY_TRACK_MODIFICATIONS = True

