from pydantic import BaseModel, EmailStr


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

# dataa_class for GenicAccount(
# inheristance
# hdfs(account_no_of thst_bank, issued_date),sbi() , etc bankk

# Trascatiion data c;lss
# ledgerc dataclss
# crete dts c;lasl of all we nned nnedde in project s