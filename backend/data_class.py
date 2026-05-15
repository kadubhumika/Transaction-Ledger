from pydantic import BaseModel, EmailStr
from datetime import datetime


class SignupData(BaseModel):

    name: str

    email: EmailStr

    password: str

    phone_no: str

    bank_name: str

    aadhaar_no: str

    account_no: str



class LoginData(BaseModel):

    email: EmailStr

    password: str


class OTPVerifyData(BaseModel):

    email: EmailStr

    otp: str

class ScheduledPaymentCreate(BaseModel):

    sender_email: str

    receiver_email: str

    amount: float

    category: str

    note: str

    scheduled_time: datetime

# dataa_class for GenicAccount(
# inheristance
# hdfs(account_no_of thst_bank, issued_date),sbi() , etc bankk

# Trascatiion data c;lss
# ledgerc dataclss
# crete dts c;lasl of all we nned nnedde in project s