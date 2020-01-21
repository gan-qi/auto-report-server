# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
from pprint import pprint

from flask import g, request, send_file
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename

from server import app, db, redis
from server.encryption import outputMD5
from server.handleExcel import handleExcel
from server.models import LOG, MAILCONFIG, TASK, USER
from server.sendMail import sendMail


api = Api(app)


def statusTrans(status):
    """转化任务状态"""
    if status == 0:
        return '未完成'
    elif status == 1:
        return '已完成'
    elif status == 2:
        return '进行中'


def handleFileStream():
    """处理文件流，整合今日和明日的任务
    """
    # 当天日期
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
    # 第二天日期
    tomorrowTime = (
        datetime.datetime.now() + datetime.timedelta(days=1)
    ).strftime("%Y-%m-%d")
    # 今日任务
    todayTasks = TASK.query.filter_by(time=str(currentTime),
            ownerId=g.userId).all()
    todayTaskList = []
    for item in todayTasks:
        node = dict(
                id=item.id,
                title=item.title,
                status=statusTrans(item.status),
                time=item.time,
                edit=False
        )
        todayTaskList.append(node)
        # 未完成任务转到明天
        if item.status != 1:
            target = TASK.query.filter_by(id=item.id).first()
            target.time = datetime.datetime.now() + datetime.timedelta(days=1)
            db.session.commit()

    # 明日任务
    tomorrowTasks = TASK.query.filter_by(time=str(tomorrowTime),
            ownerId=g.userId).all()
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
    filename = '{0}-{1}.xlsx'.format(
        g.username,
        datetime.datetime.now().strftime('%Y%m%d')
    )
    fileStream = handleExcel(g.username, todayTaskList, tomorrowTaskList)
    return fileStream, filename


@app.before_request
def before_request():
    # 此处拦截请求，验证其token
    if request.path != '/user/login':
        token = request.args.get('token')
        # 获取token来获取存储的详细用户信息
        if not token:
            return {
                'code': 50008
            }
        else:
            userInfo = redis.get(token)
            g.username = userInfo.get('username')
            g.userId = userInfo.get('id')


class submitReport(Resource):
    """将日报发送给指定邮箱
    """

    def option(self):
        return {
            'code': 20000
        }
    
    def get(self):
        fileStream, _ = handleFileStream()
        userSettings = MAILCONFIG.query.filter_by(ownerId=g.userId).first()
        if not userSettings:
            return {
                'code': 50000,
                'message': '哦豁？先去设置一下邮箱吧...'
            }
        settings = {
            'username': g.username,
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

        return send_file(
            fileStream,
            attachment_filename=filename,
            as_attachment=True
        )


class optionTask(Resource):
    """获取任务列表和新增
    """

    def option(self):
        return {
                'code': 20000
                }

    def get(self):
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
        tasks = TASK.query.filter_by(
            ownerId=g.userId,
            time=str(currentTime)
        ).all()
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
        newTask = TASK(title=data.get('title'), ownerId=g.userId)
        db.session.add(newTask)
        db.session.commit()
        targetTask = TASK.query.filter_by(
            title=data.get('title'),
            ownerId=g.userId
        ).first()
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
        mailconfig = MAILCONFIG.query.filter_by(ownerId=g.userId).first()
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
        check = MAILCONFIG.query.filter_by(ownerId=g.userId).first()
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
                        ownerId = g.userId
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
        userSettings = MAILCONFIG.query.filter_by(ownerId=g.userId).first()
        settings = {
            'username': g.username,
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
                + str(g.userId) + '.xlsx'
        file_stream = '待定'
        return send_file(
            file_stream,
            as_attachment=True,
            attachment_filename=filename
        )


class Login(Resource):
    """用户登陆
    """

    def post(self):
        data = request.get_json(force=True)
        username = data.get('username')
        password = data.get('password')
        userInfoCheck = USER.query.filter_by(
            username=username,
            password=password
        ).first()
        if not userInfoCheck:
            return {
                    'code': 40001,
                    'message': '登陆失败'
                    }
        # 加密信息获取token
        token = outputMD5('{0}{1}auto{2}'.format(
            username,
            password,
            str(time.time())
        ))
        # 将信息写入session
        redis.set(token, 
        {
            'id': userInfoCheck.id,
            'username': username
        })
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
        userInfo = redis.get(data.get('token'))
        return {
                'code': 20000,
                'data': {
                    'avatar': '...',
                    'username': userInfo.get('username')
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
