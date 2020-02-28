from server import api
from flask_restful import Resource
from flask import request
from server.sendMail import send_mail
from server.models import MAILCONFIG

import datetime


class Upload(Resource):
    """处理上传文件
    """

    def option(self):
        return {
            'code': 20000
        }

    def post(self):
        targetFile = request.files['file']
        userSettings = MAILCONFIG.query.filter_by(ownerId = g.userId).first()
        settings = {
            'username':       g.username,
            'targetUsername': userSettings.toName,
            'from_addr':      userSettings.fromEmail,
            'password':       userSettings.fromEmailKey,
            'to_addr':        userSettings.toEmail
        }
        send_mail(targetFile, settings)
        return {
            'code': 20000
        }


api.add_resource(Upload, '/uploads')
