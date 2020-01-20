# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from server.redisConn import RedisConn

import redis

app = Flask('server')
app.config.from_pyfile('config.py')

CORS(app)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)

# redis
redis = RedisConn()

from server import views, commands