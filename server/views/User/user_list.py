from server import api
from flask_restful import Resource
from server.models import User


class UserList(Resource):

    def option(self):
        return {
            'code': 20000
        }

    def get(self):
        user_list = User.query.all()
        return {
            'code': 20000,
            'data': [
                {
                    'id':       item.id,
                    'username': item.username
                }
                for item in user_list
            ]
        }


api.add_resource(UserList, '/user/list')
