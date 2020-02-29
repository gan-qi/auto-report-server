from server import api
from flask_restful import Resource
from flask import send_file, make_response
from server.utils.handle_file_stream import handle_file_stream


class OutputExcel(Resource):
    """接收前端数据，生成excel表格
    """

    def option(self):
        return {
            'code': 20000
        }

    def post(self):
        file_stream, filename = handle_file_stream()

        return send_file(
                file_stream,
                attachment_filename = filename,
                as_attachment = True
            )

        # response = make_response(send_file(file_stream))
        # response.headers["Content-Disposition"] = "attachment; filename={};".format(filename)
        # return response


api.add_resource(OutputExcel, '/outputfile')
