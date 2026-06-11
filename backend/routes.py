from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.service import AuthService

from backend.data_class import (
    SignupData,
    LoginData,
    OTPVerifyData
)

service = AuthService()
auth_router = APIRouter(prefix="/auth")


# ✅ SIGNUP
@auth_router.post("/signup")
def signup(data: SignupData, db: Session = Depends(get_db)):
    return service.signup(data, db)


# ✅ LOGIN (FIXED)
@auth_router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    return service.login(data, db)


# ✅ OTP VERIFY
@auth_router.post("/verify-otp")
async def verify_otp(data: OTPVerifyData, db: Session = Depends(get_db)):
    return await service.verify_otp(data, db)