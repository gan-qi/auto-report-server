import redis
import json


class RedisConn:

    def __init__(self):
        self.redis_conn = redis.Redis(host = 'localhost', port = '6379')

    def set(self, key, value):
        # 键，值，过期时间为一周，单位为秒
        self.redis_conn.set(key, json.dumps(value), ex = 604800)

    def get(self, key):
        value = self.redis_conn.get(key)
        try:
            return json.loads(value)
        except Exception as e:
            print(e)
            return value

    def delete(self, key):
        self.redis_conn.delete(key)

    def incr(self, key):
        self.redis_conn.incr(key)
