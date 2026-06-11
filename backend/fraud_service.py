import time
from backend.redis_cache import RedisCache
from backend.models import User
from sqlalchemy.orm import Session

cache = RedisCache()

class FraudService:

    def __init__(self):
        self.VELOCITY_LIMIT = 3          # max txns per minute
        self.AMOUNT_MULTIPLIER = 3       # anomaly threshold

    def calculate_risk(self, sender: User, receiver: User, amount: int):
        risk = 0

        # 1. Velocity Check (Redis)
        key = f"txn_count:{sender.email}"
        count = cache.get_cache(key)

        if count is None:
            count = 0
        else:
            count = int(count)

        count += 1
        cache.set_cache(key, count)
        cache.redis_client.expire(key, 60)

        if count > self.VELOCITY_LIMIT:
            risk += 40

        # 2. Amount anomaly (based on balance)
        if amount > (sender.balance * 0.5):
            risk += 30

        # 3. New recipient check
        rec_key = f"recipients:{sender.email}:{receiver.email}"
        if not cache.get_cache(rec_key):
            risk += 20
            cache.set_cache(rec_key, True)

        # 4. Large absolute transfer
        if amount > 100000:
            risk += 30

        return min(risk, 100)