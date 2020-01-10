# -*- coding: utf-8 -*-
from flask import request, send_file, session

from server import app, db
from server.models import USER, TASK, LOG, MAILCONFIG

from flask_restful import Resource, Api, reqparse
from datetime import datetime
from pprint import pprint
from werkzeug.utils import secure_filename

import os

from server.encryption import outputMD5

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
        # 检查用户名密码是否正确
        if not data.get('username'):
            return {
                    'code': 40001,
                    'message': '登陆失败'
                    }
        tokens = {
                'admin': {
                    'token': 'admin-token'
                    },
                'user': {
                    'token': 'editor-token'
                    }
                }
        print(tokens.get(data.get('username')))
        return {
                'code': 20000,
                'data': {
                    'token': tokens.get(data.get('username'))
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
        print(data)
        token = json.loads(data.get('token')).get('token')
        users = {
                'editor-token': {
                    'roles': ['editor'],
                    'introduction': '用户甲',
                    'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                    'name': '普通用户'
                    },
                'admin-token': {
                    'roles': ['admin'],
                    'introduction': '超级管理员',
                    'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                    'name': '超级管理员'
                    }
                }
        return {
                'code': 20000,
                'data': users.get(token)
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



api.add_resource(optionTask, '/task')
api.add_resource(optionOneTask, '/task/<int:taskid>')
api.add_resource(mailConfig, '/mailconfig')
api.add_resource(Upload, '/uploads')
api.add_resource(Login, '/user/login')
api.add_resource(userInfo, '/user/info')
api.add_resource(Logout, '/user/logout')
