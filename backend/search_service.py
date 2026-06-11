from sqlalchemy.orm import Session
from backend.models import User
from backend.bank_account_models import BankAccount  # Imported bank account model
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
            User.email.ilike(f"%{query}%")
        ).all()

        result = []

        for user in users:
            # Query the active bank account details for this user
            account = db.query(BankAccount).filter(
                BankAccount.user_email == user.email,
                BankAccount.is_active == True
            ).first()

            result.append({
                "name": user.name,
                "email": user.email,
                "bank_name": account.bank_name if account else "N/A",
                "balance": account.balance if account else 0,
                "account_no": account.account_no if account else "N/A"
            })

        cache.set_cache(
            f"search:{query}",
            result
        )

        return {
            "source": "postgres",
            "users": result
        }
