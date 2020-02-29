from server import api, db
from flask_restful import Resource
from flask import request
from server.models import Task


class OptionOneTomorrowTask(Resource):
    """对单个任务进行删除和修改
    """

    def option(self):
        return {
            'code': 20000
        }

    def delete(self, taskid):
        target_task = Task.query.filter_by(id = taskid).first()
        db.session.delete(target_task)
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
        new_task = Task.query.filter_by(id = taskid).first()
        new_task.title = data.get('title')
        new_task.status = data.get('status')
        db.session.commit()
        return {
            'code': 20000
        }


api.add_resource(OptionOneTomorrowTask, '/tomorrowtask/<int:taskid>')
