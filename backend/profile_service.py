from sqlalchemy.orm import Session

from backend.models import User

class ProfileService:
    def get_profile(self, email,db: Session):
        user = db.query(User).filter(User.email==email).first()

        if not user:
            return {"error":"User not found"}
        return {
            "name": user.name,
            "email": user.email,
            "phone_no": user.phone_no,
            "bank_name": user.bank_name,
            "account_no": user.account_no,
            "balance": user.balance,
            "is_verified": user.is_verified
        }

    def update_profile(
            self,
            email,
            data,
            db: Session
    ):

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            return {"error": "User not found"}

        user.name = data.name
        user.phone_no = data.phone_no
        user.bank_name = data.bank_name

        db.commit()

        return {
            "message": "Profile updated successfully"
        }

    def add_balance(
            self,
            email,
            amount,
            db: Session
    ):

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            return {"error": "User not found"}

        user.balance += amount

        db.commit()

        return {
            "message": "Balance added successfully",
            "updated_balance": user.balance
        }