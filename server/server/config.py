# -*- coding: utf-8 -*-
import os
import sys
import redis

from server import app

SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

# redis
SESSION_TYPE = 'redis'  # session类型为redis
SESSION_PERMANENT = False  # 如果设置为True，则关闭浏览器session就失效。
SESSION_USE_SIGNER = False  # 是否对发送到浏览器上session的cookie值进行加密
SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀
SESSION_REDIS = redis.Redis(host='192.168.1.150', port='6379')  # 用于连接redis的配置


# sqlite3
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

