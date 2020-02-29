from server import api, db
from server.models import Other
from flask import request, g
from flask_restful import Resource

import datetime


class Advice(Resource):

    def __init__(self):
        self.current_time = datetime.datetime.now().strftime('%Y-%m-%d')

    def option(self):
        return {
            'code': 20000
        }

    def get(self):
        advice = Other.query.filter_by(
            ownerId = g.userId,
            time = str(self.current_time)
        ).first()
        if advice:
            data = advice.advice
        else:
            data = ''
        return {
            'code': 20000,
            'data': data
        }

    def post(self):
        data = request.get_json(force = True)
        advice = data.get('advice')
        check_advice = Other.query.filter_by(
            ownerId = g.userId,
            time = str(self.current_time)
        ).first()
        if check_advice:
            check_advice.advice = advice
        else:
            new_advice = Other(
                advice = advice,
                ownerId = g.userId
            )
            db.session.add(new_advice)
        db.session.commit()
        return {
            'code': 20000
        }


api.add_resource(Advice, '/advice')
