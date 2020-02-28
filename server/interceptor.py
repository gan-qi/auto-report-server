from server import app, redis
from flask import request, g


@app.before_request
def before_request():
    # 此处拦截请求，验证其token
    white_list = [
        '/user/login'
    ]
    if request.path not in white_list:
        # 获取token来获取存储的详细用户信息
        token = request.args.get('token')

        if not token:
            return {
                'code': 50008
            }
        else:
            user_info = redis.get(token)
            g.token = token
            g.username = user_info.get('username')
            g.userId = user_info.get('id')
