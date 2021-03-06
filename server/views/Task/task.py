from server import api, db
from server.models import Task, User
from flask import request, g
from flask_restful import Resource

import datetime


def trans_user_id(owner_id, owner_name, from_user_id):
    if from_user_id != owner_id:
        return User.query.filter_by(id = from_user_id).first().username
    return owner_name


class OptionTask(Resource):
    """获取任务列表和新增
    """

    def option(self):
        return {
            'code': 20000
        }

    def get(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        tasks = Task.query.filter_by(
            ownerId = g.userId,
            time = str(current_time)
        ).all()
        task_list = [
            dict(
                id = item.id,
                title = item.title,
                owner_username = item.owner.username,
                from_username = trans_user_id(item.id, item.owner.username, item.from_user_id),
                status = item.status,
                time = item.time,
                edit = False
            )
            for item in tasks
        ]
        return {
            'code': 20000,
            'data': task_list
        }

    def post(self):
        """新增任务

        data: {
            'user_list': [
                {
                    'id': 1,
                    'username': 'tom'
                }
            ]
            'title': 'xxx',
        }
        """
        data = request.get_json(force = True)
        user_list = data.get('user_list')
        for user in user_list:
            new_task = Task(title = data.get('title'), ownerId = user.get('id'), from_user_id = g.userId)
            db.session.add(new_task)
        db.session.commit()
        target_task = Task.query.filter_by(
            title = data.get('title'),
            ownerId = g.userId
        ).first()
        return {
            'code': 20000,
            # 返回新增任务的id
            'data': target_task.id
        }


api.add_resource(OptionTask, '/task')
