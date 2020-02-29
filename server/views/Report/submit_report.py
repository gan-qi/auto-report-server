from server import api
from server.models import MailConfig
from server.utils.handle_file_stream import handle_file_stream
from server.utils.sendMail import send_mail
from flask_restful import Resource
from flask import g


class SubmitReport(Resource):
    """将日报发送给指定邮箱
    """

    def option(self):
        return {
            'code': 20000
        }

    def post(self):
        file_stream, _ = handle_file_stream()
        user_settings = MailConfig.query.filter_by(ownerId = g.userId).first()
        if not user_settings:
            return {
                'code':    50000,
                'message': '哦豁？先去设置一下邮箱吧...'
            }
        settings = {
            'username':       g.username,
            'targetUsername': user_settings.toName,
            'from_addr':      user_settings.fromEmail,
            'password':       user_settings.fromEmailKey,
            'to_addr':        user_settings.toEmail
        }
        send_mail(file_stream, settings)
        return {
            'code': 20000
        }


api.add_resource(SubmitReport, '/submitreport')
