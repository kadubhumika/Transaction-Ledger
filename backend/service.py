from sqlalchemy.orm import Session
from backend.models import User
from backend.auth import SignupValidator
from backend.core import (
    hash_password,
    verify_password,
    generate_otp,
    create_jwt
)
from backend.redis_client import redis_client
from backend.email_service import send_email_otp
from backend.websocket_manager import manager

validator = SignupValidator()

class AuthService:

    def signup(self, data, db: Session):

        valid, message = validator.validate(data)

        if not valid:
            return {"error": message}

        hashed_password = hash_password(data.password)

        user = User(
            name=data.name,
            email=data.email,
            password=hashed_password,
            phone_no=data.phone_no,
            aadhaar_no=data.aadhaar_no,
            account_no=data.account_no,
            bank_name=data.bank_name
        )

        db.add(user)
        db.commit()

        return {
            "message": "Signup successful"
        }

    def login(self, data, db: Session):

        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if not user:
            return {"error": "User not found"}

        if not verify_password(
            data.password,
            user.password
        ):
            return {"error": "Incorrect password"}

        otp = generate_otp()

        # Decoding/Encoding handling might be needed depending on your redis_client version
        redis_client.setex(
            f"otp:{user.email}",
            300,
            otp
        )

        send_email_otp(user.email, otp)

        return {
            "message": "OTP sent"
        }

    async def verify_otp(self, data, db: Session):

        saved_otp = redis_client.get(
            f"otp:{data.email}"
        )

        if saved_otp != data.otp:
            return {"error": "Invalid OTP"}

        user = db.query(User).filter(
            User.email == data.email
        ).first()

        user.is_verified = True

        db.commit()

        token = create_jwt(user.email)


        await manager.send_message(
            user.email,
            "Login successful"
        )

        return {
            "message": "OTP verified",
            "token": token
        }


# service.py
# thisis main part here we will add app apus cotre logic function = coonect websocket + redis all system idea all this
# def tarnsction_logicv()
# def send_money ()
# # reciptfunction(0) suufeull
# and noticiation_fynction() for arch we will add notifaicyion vai wesocket + daily unadte liek rbi adde4e this faetyures
#sbi ad etc liek

