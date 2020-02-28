from server import api
from flask_restful import Resource
from flask import send_file
from server.utils.handle_file_stream import handleFileStream


class outputExcel(Resource):
    """接收前端数据，生成excel表格
    """

    def option(self):
        return {
            'code': 20000
        }

    def get(self):
        fileStream, filename = handleFileStream()

        return send_file(
            fileStream,
            attachment_filename = filename,
            as_attachment = True
        )


api.add_resource(outputExcel, '/outputfile')
