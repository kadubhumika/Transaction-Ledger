from sqlalchemy.orm import Session

from backend.models import User

from backend.redis_cache import RedisCache

cache = RedisCache()


class SearchService:

    def search_user(self, query: str, db: Session):

        cached_users = cache.get_cache(
            f"search:{query}"
        )

        if cached_users:

            return {
                "source": "redis cache",
                "users": cached_users
            }

        users = db.query(User).filter(
            User.name.ilike(f"%{query}%") |
            User.email.ilike(f"%{query}%") |
            User.bank_name.ilike(f"%{query}%")
        ).all()

        result = []

        for user in users:

            result.append({
                "name": user.name,
                "email": user.email,
                "bank_name": user.bank_name,
                "balance": user.balance,
                "account_no": user.account_no
            })

        cache.set_cache(
            f"search:{query}",
            result
        )

        return {
            "source": "postgres",
            "users": result
        }