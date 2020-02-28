from server import api
from server.models import MAILCONFIG
from server.utils.handle_file_stream import handleFileStream
from server.sendMail import send_mail
from flask_restful import Resource


class submitReport(Resource):
    """将日报发送给指定邮箱
    """

    def option(self):
        return {
            'code': 20000
        }

    def get(self):
        file_stream, _ = handleFileStream()
        user_settings = MAILCONFIG.query.filter_by(ownerId = g.userId).first()
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


api.add_resource(submitReport, '/submitreport')
