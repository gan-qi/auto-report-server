from server import api
from flask_restful import Resource
from flask import send_file, request, g

import datetime


class Downloads(Resource):
    """提供文件下载
    """

    def option(self):
        return {
            'code': 20000
        }

    def post(self):
        data = request.get_json(force = True)
        # 生成文件...
        filename = str(datetime.datetime.now().strftime('%Y-%m-%d')) \
                   + str(g.userId) + '.xlsx'
        file_stream = '待定'
        return send_file(
            file_stream,
            as_attachment = True,
            attachment_filename = filename
        )
