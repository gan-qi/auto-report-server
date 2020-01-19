# -*- coding: utf-8 -*-
from flask import request, send_file, session

from server import app, db
from server.models import USER, TASK, LOG, MAILCONFIG

from flask_restful import Resource, Api, reqparse
from pprint import pprint
from werkzeug.utils import secure_filename

import os
import datetime
import json

from server.encryption import outputMD5
from server.handleExcel import handleExcel
from server.sendMail import sendMail

api = Api(app)


username = 'tom'
userId = 1

def handleFileStream():
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
    # 完成状态转换
    statusTrans = lambda status: '完成' if status else '未完成'
    # 今日任务
    todayTasks = TASK.query.filter_by(time=str(currentTime),
            ownerId=userId).all()
    todayTaskList = [
            dict(
                id=item.id,
                title=item.title,
                status=statusTrans(item.status),
                time=item.time,
                edit=False
                )
            for item in todayTasks
            ]
    # 明日任务
    tomorrowTime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrowTasks = TASK.query.filter_by(time=str(tomorrowTime),
            ownerId=userId).all()
    tomorrowTaskList = [
            dict(
                id=item.id,
                title=item.title,
                status=statusTrans(item.status),
                time=item.time,
                edit=False
                )
            for item in tomorrowTasks
            ]
    filename = '{0}-{1}.xlsx'.format(username, datetime.datetime.now().strftime('%Y%m%d'))
    fileStream = handleExcel(username, todayTaskList, tomorrowTaskList)
    return fileStream, filename


@app.before_request
def before_request():
    print('before_request: ', session)

class submitReport(Resource):
    """将日报发送给指定邮箱
    """

    def option(self):
        return {
            'code': 20000
        }
    
    def get(self):
        fileStream, _ = handleFileStream()
        userSettings = MAILCONFIG.query.filter_by(ownerId=userId).first()
        settings = {
            'username': username,
            'targetUsername': userSettings.toName,
            'from_addr': userSettings.fromEmail,
            'password': userSettings.fromEmailKey,
            'to_addr': userSettings.toEmail
        }
        sendMail(fileStream, settings)
        return {
            'code': 20000
        }


class outputExcel(Resource):
    """接收前端数据，生成excel表格
    """

    def option(self):
        return {
                'code': 20000
                }

    def get(self):
        fileStream, filename = handleFileStream()

        return send_file(fileStream, attachment_filename=filename, as_attachment=True)


class optionTask(Resource):
    """获取任务列表和新增
    """

    def option(self):
        return {
                'code': 20000
                }

    def get(self):
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
        tasks = TASK.query.filter_by(ownerId=userId, time=str(currentTime)).all()
        taskList = [
                dict(
                    id=item.id,
                    title=item.title,
                    status=item.status,
                    time=item.time,
                    edit=False
                    )
                for item in tasks
                ]

        print('test:  ', session.get('f5c11655e04eff9f837a2833fa150d6e', 'no set'))
        return {
                    'code': 20000,
                    'data': taskList
                }

    def post(self):
        """新增任务

        data: {
            'title': 'xxx',
        }
        """
        data = request.get_json(force=True)
        newTask = TASK(title=data.get('title'), ownerId=1)
        db.session.add(newTask)
        db.session.commit()
        targetTask = TASK.query.filter_by(title=data.get('title'), ownerId=1).first()
        return {
                    'code': 20000,
                    # 返回新增任务的id
                    'data': targetTask.id
                }


class optionOneTask(Resource):
    """对单个任务进行删除和修改
    """

    def option(self):
        return {
                    'code': 20000
                }

    def delete(self, taskid):
        targetTask = TASK.query.filter_by(id=taskid).first()
        db.session.delete(targetTask)
        db.session.commit()
        return {
                    'code': 20000
                }

    def post(self, taskid):
        """修改任务

        data: {
            'id': 1,
            'title': 'xxx',
            'status': True
        }
        """
        data = request.get_json(force=True)
        newTask = TASK.query.filter_by(id=taskid).first()
        newTask.title = data.get('title')
        newTask.status = data.get('status')
        db.session.commit()
        return {
                    'code': 20000
                }


class mailConfig(Resource):
    """邮箱设置，接受前端发来的邮箱信息放到数据库
    """

    def option(self):
        return {
                'code': 20000
                }

    def get(self):
        """获取邮箱设置
        """
        mailconfig = MAILCONFIG.query.filter_by(ownerId=userId).first()
        if mailconfig:
            data = {
                    'fromName': mailconfig.fromName,
                    'toName': mailconfig.toName,
                    'fromEmail': mailconfig.fromEmail,
                    'fromEmailKey': mailconfig.fromEmailKey,
                    'toEmail': mailconfig.toEmail
                    }
        else:
            data = {
                    'fromName': '',
                    'toName': '',
                    'fromEmail': '',
                    'fromEmailKey': '',
                    'toEmail': ''
                    }
        return {
                'code': 20000,
                'data': data
                }


    def post(self):
        """
        data = {
            'fromName': '',
            'toName': '',
            'fromEmail': '',
            'fromEmailKey': '',
            'toEmail': ''
        }
        """
        data = request.get_json(force=True)
        # 先判断该用户设置是否存在
        check = MAILCONFIG.query.filter_by(ownerId=userId).first()
        if check:
            check.fromName = data.get('fromName')
            check.toName = data.get('toName')
            check.fromEmail = data.get('fromEmail')
            check.fromEmailKey = data.get('fromEmailKey')
            check.toEmail = data.get('toEmail')
        else:
            config = MAILCONFIG(
                        fromName = data.get('fromName'),
                        toName = data.get('toName'),
                        fromEmail = data.get('fromEmail'),
                        fromEmailKey = data.get('fromEmailKey'),
                        toEmail = data.get('toEmail'),
                        ownerId = userId
                    )
            db.session.add(config)
        db.session.commit()
        return {
                'code': 20000
                }


class Upload(Resource):
    """处理上传文件
    """

    def option(self):
        return {
                'code': 20000
                }

    def post(self):
        targetFile = request.files['file']
        userSettings = MAILCONFIG.query.filter_by(ownerId=userId).first()
        settings = {
            'username': username,
            'targetUsername': userSettings.toName,
            'from_addr': userSettings.fromEmail,
            'password': userSettings.fromEmailKey,
            'to_addr': userSettings.toEmail
        }
        sendMail(targetFile, settings)
        return {
                'code': 20000
                }


class Downloads(Resource):
    """提供文件下载
    """

    def option(self):
        return {
                'code': 20000
                }

    def post(self):
        data = request.get_json(force=True)
        # 生成文件...
        filename = str(datetime.datetime.now().strftime('%Y-%m-%d')) \
                + str(userId) + '.xlsx'
        file_stream = '待定'
        return send_file(file_stream, as_attachment=True, attachment_filename=filename)


class Auth(Resource):
    """用户认证
    """

    def option(self):
        return {
                'code': 20000
                }

    def post(self):
        data = request.get_json(force=True)
        username = data.get('username')
        password = data.get('password')
        userInfo = USER.query.filter_by(username=username).first()
        # 先判断用户名
        if userInfo:
            # 再判断用户的密码
            if userInfo.password != password:
                return {
                        'code': 20001,
                        'message': '密码错误'
                        }
            else:
                # 生成token放到session
                token = outputMD5(username[1:] + password)
                session['username'] = username
                session['token'] = token
                # 设置有效期为一个月
                session.permanent = True
                return {
                        'code': 20000,
                        'token': token
                        }
        else:
            return {
                    'code': 20001,
                    'message': '用户名不存在'
                    }


class Login(Resource):
    """用户登陆
    """

    def post(self):
        data = request.get_json(force=True)
        if not data.get('username'):
            return {
                    'code': 40001,
                    'message': '登陆失败'
                    }
        print(data.get('username'), data.get('password'))
        # 加密信息获取token
        token = outputMD5('{0}auto{1}'.format(
            data.get('username'),
            data.get('password'))
        )
        # 将信息写入session
        session[token] = {
            'username': data.get('username'),
            'password': data.get('password')
        }
        session['key'] = 'value'
        return {
                'code': 20000,
                'data': {
                    'token': token
                    }
                }


class userInfo(Resource):
    """获取用户信息
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str)

    def get(self):
        data = self.parser.parse_args()
        token = data.get('token')
        # userInfo = session.get(token, 'not set')
        print('session key:', session.get('key', 'not set'))
        return {
                'code': 20000,
                'data': {
                    'avatar': '...',
                    'username': 'tom'
                    }
                }


class Logout(Resource):
    """登出
    input: b''
    ouput: {
        'code': 20000,
        'data': 'success'
    }
    """
    def post(self):
        return {
                'code': 20000,
                'data': 'success'
                }


api.add_resource(submitReport, '/submitreport')
api.add_resource(outputExcel, '/outputfile')
api.add_resource(optionTask, '/task')
api.add_resource(optionOneTask, '/task/<int:taskid>')
api.add_resource(mailConfig, '/mailconfig')
api.add_resource(Upload, '/uploads')
api.add_resource(Login, '/user/login')
api.add_resource(userInfo, '/user/info')
api.add_resource(Logout, '/user/logout')
