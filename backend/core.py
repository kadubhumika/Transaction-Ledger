import re
import random

from jose import jwt


SECRET_KEY = "mysecret"

ALGORITHM = "HS256"


def validate_password(password):

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    return True


def validate_accountNo(accountNo):

    acc_str = str(accountNo)

    if not acc_str.isnumeric():
        return False, "Account number must contain only digits."

    if not (5 <= len(acc_str) <= 17):
        return False, "Account number must be between 5 and 17 digits."

    return True, "Valid account number."



def validate_aadhaar(aadhaar):

    return len(aadhaar) == 12 and aadhaar.isdigit()


def hash_password(password):

    return "hashed_" + password


def verify_password(password, hashed):

    return hashed == "hashed_" + password


import secrets
import string

def generate_otp(length=6):

    digits = string.digits
    otp = ''.join(secrets.choice(digits) for _ in range(length))
    return otp

def validate_accountNo(account_no):

    return (
        account_no.isdigit()
        and len(account_no) >= 10
    )

def create_jwt(email):

    payload = {"email": email}

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# core fule
# here we will create backened engine base model so that we can ad d esaily redis logic + websocket logic to all faetures esaliy
# example
# redis_client = redis logic funcion
# wesocket_client= wesocket logic function
#then now we can direcly user redis_cleint , wesoket_cleint ebrywhere
