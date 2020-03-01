from server import api, redis
from flask_restful import Resource
from flask import request, g
from server.models import User
from server.utils.encryption import outputMD5
import time


class Login(Resource):
    """用户登陆
    """

    def post(self):
        data = request.get_json(force = True)
        username = data.get('username')
        password = data.get('password')
        user_info_check = User.query.filter_by(
            username = username,
            password = password
        ).first()
        if not user_info_check:
            return {
                'code':    40001,
                'message': '登陆失败'
            }
        # 加密信息获取token
        token = outputMD5('{0}{1}auto{2}'.format(
            username,
            password,
            str(time.time())
        ))
        # 将信息写入redis
        redis.set(token,
                  {
                      'id':       user_info_check.id,
                      'username': username,
                      'role':     user_info_check.role
                  })
        return {
            'code': 20000,
            'data': {
                'token': token
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
        redis.delete(g.token)
        return {
            'code': 20000,
            'data': 'success'
        }


api.add_resource(Login, '/user/login')
api.add_resource(Logout, '/user/logout')
