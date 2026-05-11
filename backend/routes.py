# now iin nrouyres ist comes alll logic ccalling via endpoints for evry faeture work task all
# routes for all authtication part signup , otp send , save , login all flow
# routes for transcation part liek send money , money recaieved all ceck bakacned , check history , and as we willl add serch by nmae to pay money if user serch
# Ra so ut should show rahul sharmand by clickingiyt should send moeyy
# soo for now we wull add stimulated csv file for db user basically user (info- name, email , password , phoeno, addhar_no)
# sio that it will besscy for project
# recipt suuceful recipt api

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.service import AuthService

from backend.data_class import (
    SignupData,
    LoginData,
    OTPVerifyData
)


router = APIRouter()

service = AuthService()


@router.post("/auth/signup")
def signup(
    data: SignupData,
    db: Session = Depends(get_db)
):

    return service.signup(data, db)


@router.post("/auth/login")
def login(
    data: LoginData,
    db: Session = Depends(get_db)
):

    return service.login(data, db)


@router.post("/auth/verify-otp")
async def verify_otp(
    data: OTPVerifyData,
    db: Session = Depends(get_db)
):

    return await service.verify_otp(data, db)