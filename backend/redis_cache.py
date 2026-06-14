import os
import json
import redis

class RedisCache:
    def __init__(self):
        redis_url = os.environ.get("REDIS_URL")
        if redis_url:
            self.redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
        else:
            self.redis_client = redis.Redis(
                host="localhost",
                port=6380,
                decode_responses=True
            )

    def save_balance(self, email, balance):
        self.redis_client.set(f"balance:{email}", balance)

    def get_balance(self, email):
        return self.redis_client.get(f"balance:{email}")

    def save_cache(self, key, data):
        self.redis_client.set(key, json.dumps(data), ex=300)

    def set_cache(self, key, value):
        self.redis_client.set(key, json.dumps(value))

    def get_cache(self, key):
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def delete_cache(self, key):
        return self.redis_client.delete(key)
