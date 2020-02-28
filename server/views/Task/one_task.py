from server import api, db
from flask_restful import Resource
from flask import request
from server.models import TASK


class optionOneTask(Resource):
    """对单个任务进行删除和修改
    """

    def option(self):
        return {
            'code': 20000
        }

    def delete(self, taskid):
        targetTask = TASK.query.filter_by(id = taskid).first()
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
        data = request.get_json(force = True)
        newTask = TASK.query.filter_by(id = taskid).first()
        newTask.title = data.get('title')
        newTask.status = data.get('status')
        db.session.commit()
        return {
            'code': 20000
        }


api.add_resource(optionOneTask, '/task/<int:taskid>')
