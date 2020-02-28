from server import api
from server.models import TASK
from flask import request
from flask_restful import Resource

import datetime


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
            ownerId = g.userId,
            time = str(currentTime)
        ).all()
        taskList = [
            dict(
                id = item.id,
                title = item.title,
                status = item.status,
                time = item.time,
                edit = False
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
        data = request.get_json(force = True)
        newTask = TASK(title = data.get('title'), ownerId = g.userId)
        db.session.add(newTask)
        db.session.commit()
        targetTask = TASK.query.filter_by(
            title = data.get('title'),
            ownerId = g.userId
        ).first()
        return {
            'code': 20000,
            # 返回新增任务的id
            'data': targetTask.id
        }


api.add_resource(optionTask, '/task')
