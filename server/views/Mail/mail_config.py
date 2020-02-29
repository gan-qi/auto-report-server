from server import api, db
from flask_restful import Resource
from flask import request, g
from server.models import MailConfig


class MailConfigClass(Resource):
    """邮箱设置，接受前端发来的邮箱信息放到数据库
    """

    def option(self):
        return {
            'code': 20000
        }

    def get(self):
        """获取邮箱设置
        """
        mail_config = MailConfig.query.filter_by(ownerId = g.userId).first()
        if mail_config:
            data = {
                'fromName':     mail_config.fromName,
                'toName':       mail_config.toName,
                'fromEmail':    mail_config.fromEmail,
                'fromEmailKey': mail_config.fromEmailKey,
                'toEmail':      mail_config.toEmail
            }
        else:
            data = {
                'fromName':     '',
                'toName':       '',
                'fromEmail':    '',
                'fromEmailKey': '',
                'toEmail':      ''
            }
        return {
            'code': 20000,
            'data': data
        }

    def post(self):
        """
        data = {
            'fromName': '',
            'toName': '',
            'fromEmail': '',
            'fromEmailKey': '',
            'toEmail': ''
        }
        """
        data = request.get_json(force = True)
        # 先判断该用户设置是否存在
        check = MailConfig.query.filter_by(ownerId = g.userId).first()
        if check:
            check.fromName = data.get('fromName')
            check.toName = data.get('toName')
            check.fromEmail = data.get('fromEmail')
            check.fromEmailKey = data.get('fromEmailKey')
            check.toEmail = data.get('toEmail')
        else:
            config = MailConfig(
                fromName = data.get('fromName'),
                toName = data.get('toName'),
                fromEmail = data.get('fromEmail'),
                fromEmailKey = data.get('fromEmailKey'),
                toEmail = data.get('toEmail'),
                ownerId = g.userId
            )
            db.session.add(config)
        db.session.commit()
        return {
            'code': 20000
        }


api.add_resource(MailConfigClass, '/mailconfig')
