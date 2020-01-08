# -*- coding: utf-8 -*-
from flask import request, send_file

from server import app, db
from server.models import USER, TASK, LOG, MAILCONFIG

from flask_restful import Resource, Api, reqparse
from datetime import datetime
from pprint import pprint
from werkzeug.utils import secure_filename

import os

api = Api(app)


username = 'tom'
userId = 1

class optionTask(Resource):
    """获取任务列表和新增
    """

    def option(self):
        return {
                'code': 20000
                }

    def get(self):
        currentTime = datetime.now().strftime('%Y-%m-%d')
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
        return {
                    'code': 20000
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
        targetFile.save(os.path.join(app.root_path + '/uploads',
            targetFile.filename))
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
        filename = str(datetime.now().strftime('%Y-%m-%d')) \
                + str(userId) + '.xlsx'
        file_stream = '待定'
        return send_file(file_stream, as_attachment=True, attachment_filename=filename)


api.add_resource(optionTask, '/task')
api.add_resource(optionOneTask, '/task/<int:taskid>')
api.add_resource(mailConfig, '/mailconfig')
api.add_resource(Upload, '/uploads')
