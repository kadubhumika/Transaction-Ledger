import os
import redis

redis_url = os.environ.get("REDIS_URL")

if redis_url:
    redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
else:
    redis_client = redis.Redis(
        host="localhost",
        port=6380,
        decode_responses=True
    )
