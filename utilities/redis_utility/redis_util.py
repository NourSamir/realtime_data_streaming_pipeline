from redis import Redis
from utilities.redis_utility.configs import *

class RedisUtility:
    def __init__(self):
        self.client = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True
        )

    def init_empty_dict(self, dict_name):
        # initial_value = {'_trick': None}
        # self.client.hmset(dict_name, initial_value)
        self.client.hset(dict_name, '_trick', -1)

    def insert_to_dict(self, dict_name, key, value):
        self.client.hset(dict_name, key=key, value=value)

    def get_from_dict(self, dict_name, key):
        return self.client.hget(dict_name, key)

    def delete_from_dict(self, dict_name, key):
        self.client.hdel(dict_name, key)

    def is_dict_key_exist(self, dict_name, key):
        return self.client.hexists(dict_name, key)

    def is_dict_exist(self, dict_name):
        return self.client.exists(dict_name)

    def get_dict(self, dict_name):
        _dict = self.client.hgetall(dict_name)
        # return json.loads(_dict)
        return _dict

    def delete_dict(self, dict_name):
        self.client.delete(dict_name)
