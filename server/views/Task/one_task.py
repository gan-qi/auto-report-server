from server import api, db
from flask_restful import Resource
from flask import request
from server.models import Task


class OptionOneTask(Resource):
    """对单个任务进行删除和修改
    """

    def option(self):
        return {
            'code': 20000
        }

    def delete(self, taskid):
        target_task = Task.query.filter_by(id = taskid).first()
        mult_tasks = Task.query.filter_by(
            title = target_task.title,
            from_user_id = target_task.ownerId
        ).all()
        for task in mult_tasks:
            db.session.delete(task)
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
        data = request.get_json(force = True)
        target_task = Task.query.filter_by(id = taskid).first()
        mult_tasks = Task.query.filter_by(
            title = target_task.title,
            from_user_id = target_task.ownerId
        ).all()
        for task in mult_tasks:
            task.title = data.get('title')
            task.status = data.get('status')
        db.session.commit()
        return {
            'code': 20000
        }


api.add_resource(OptionOneTask, '/task/<int:taskid>')
