# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api

from server.utils.redisConn import RedisConn

app = Flask('server')
app.config.from_pyfile('config.py')

CORS(app)
db = SQLAlchemy(app)
api = Api(app)
redis = RedisConn()

from server import commands
from server import interceptor
from server.views.User import auth, info, user_list
from server.views.Task import one_task, task, tomorrow_task, one_tomorrow_task, advice
from server.views.Report import submit_report
from server.views.Mail import mail_config
from server.views.File import download, uploads, output_excel
