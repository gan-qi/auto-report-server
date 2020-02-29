from server import api
from flask_restful import Resource
from flask import request, g
from server.utils.sendMail import send_mail
from server.models import MailConfig


class Upload(Resource):
    """处理上传文件
    """

    def option(self):
        return {
            'code': 20000
        }

    def post(self):
        target_file = request.files['file']
        user_settings = MailConfig.query.filter_by(ownerId = g.userId).first()
        settings = {
            'username':       g.username,
            'targetUsername': user_settings.toName,
            'from_addr':      user_settings.fromEmail,
            'password':       user_settings.fromEmailKey,
            'to_addr':        user_settings.toEmail
        }
        send_mail(target_file, settings)
        return {
            'code': 20000
        }


api.add_resource(Upload, '/uploads')
