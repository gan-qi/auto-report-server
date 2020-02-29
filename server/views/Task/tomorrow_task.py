from server import api, db
from server.models import Task
from flask import request, g
from flask_restful import Resource

import datetime


class OptionTomorrowTask(Resource):
    """获取任务列表和新增
    """

    def __init__(self):
        self.tomorrow_time = (
                datetime.datetime.now() + datetime.timedelta(days = 1)
        ).strftime("%Y-%m-%d")

    def option(self):
        return {
            'code': 20000
        }

    def get(self):
        tasks = Task.query.filter_by(
            ownerId = g.userId,
            time = str(self.tomorrow_time)
        ).all()
        task_list = [
            dict(
                id = item.id,
                title = item.title,
                status = item.status,
                time = self.tomorrow_time,
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
            'title': 'xxx',
        }
        """
        data = request.get_json(force = True)
        new_task = Task(
            title = data.get('title'),
            time = self.tomorrow_time,
            ownerId = g.userId
        )
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


api.add_resource(OptionTomorrowTask, '/tomorrowtask')
