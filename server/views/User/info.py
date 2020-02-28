from server import api, redis
from flask_restful import Resource, reqparse


class UserInfo(Resource):
    """获取用户信息
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type = str)

    def get(self):
        data = self.parser.parse_args()
        user_info = redis.get(data.get('token'))
        return {
            'code': 20000,
            'data': {
                'avatar':   '...',
                'username': user_info.get('username')
            }
        }


api.add_resource(UserInfo, '/user/info')
