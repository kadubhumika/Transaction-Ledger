from sqlalchemy.orm import Session
from backend.models import User
from backend.bank_account_models import BankAccount
from backend.redis_client import redis_client


class ProfileService:

    def get_profile(self, email, db: Session):
        user = db.query(User).filter(User.email == email).first()

        account = db.query(BankAccount).filter(
            BankAccount.user_email == email,
            BankAccount.is_active == True
        ).first()

        if not user:
            return {"error": "User not found"}

        return {
            "name": user.name,
            "email": user.email,
            "phone_no": user.phone_no,
            "bank_name": account.bank_name if account else None,
            "account_no": account.account_no if account else None,
            "balance": account.balance if account else 0,
            "is_verified": user.is_verified
        }

    def update_profile(self, email, data, db: Session):

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return {"error": "User not found"}

        user.name = data.name
        user.phone_no = data.phone_no
        user.bank_name = data.bank_name

        db.commit()

        return {"message": "Profile updated successfully"}

    def add_balance(self, email, amount, db: Session):
        account = db.query(BankAccount).filter(
            BankAccount.user_email == email,
            BankAccount.is_active == True
        ).first()

        if not account:
            return {"error": "Active account not found"}

        account.balance += amount
        db.commit()


        for key in redis_client.scan_iter("search:*"):
            redis_client.delete(key)

        # 🚀 ADD THIS LINE RIGHT HERE TO EVICT CACHE:
        from backend.redis_cache import RedisCache
        RedisCache().delete_cache(f"profile:{email}")

        return {
            "message": "Balance added successfully",
            "updated_balance": account.balance
        }
