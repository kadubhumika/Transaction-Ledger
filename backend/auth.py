# First Step is Auth files
# Here we will create simple Authtication flow
# Function def signup for(name, email , password , phoeno, addhar_no) this feild must be extenstion properly like password must be strong , addhar_no must be of 12 digit etc email musr be of crt format alll
# save this all in postgresql User table
# Function for login (with email+password+phoneno) so that otp will send to eamil or via phone no to verfy accoynr)
# fumctio for otp verification via websocket or backened
from datetime import datetime
from pydantic import BaseModel, EmailStr

from pydantic import BaseModel, EmailStr
from backend.core import (
    validate_password,
    validate_aadhaar,
    validate_accountNo
)

class SignupValidator:
    def validate(self, data):
        if not validate_password(data.password):
            return False, "Weak password"
        if not validate_aadhaar(data.aadhaar_no):
            return False, "Invalid Aadhaar"
        if not validate_accountNo(data.account_no):
            return False, "Invalid account number"
        return True, "Validation successful"

# this accound shpuld be svae in postgres database