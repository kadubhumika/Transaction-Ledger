from backend.database import SessionLocal

from backend.models import User

db = SessionLocal()

users = [

    User(
        name="Rahul Sharma",
        email="rahul@gmail.com",
        password="123",
        phone_no="9999999991",
        aadhaar_no="111122223333",
        bank_name="SBI",
        account_no="10001",
        balance=50000,
        is_verified=True
    ),

    User(
        name="Priya Verma",
        email="priya@gmail.com",
        password="123",
        phone_no="9999999992",
        aadhaar_no="111122223334",
        bank_name="HDFC",
        account_no="10002",
        balance=45000,
        is_verified=True
    ),
    User(
        name="Aniket Deshmukh",
        email="aniket.d@outlook.com",
        password="123",
        phone_no="9881234567",
        aadhaar_no="222233334444",
        bank_name="ICICI",
        account_no="10003",
        balance=75000,
        is_verified=True
    ),
    User(
        name="Sneha Patil",
        email="sneha.p@yahoo.com",
        password="123",
        phone_no="9765432109",
        aadhaar_no="333344445555",
        bank_name="Axis Bank",
        account_no="10004",
        balance=32000,
        is_verified=True
    ),
    User(
        name="Vikram Singh",
        email="vikram.singh@gmail.com",
        password="123",
        phone_no="9123456780",
        aadhaar_no="444455556666",
        bank_name="Bank of Baroda",
        account_no="10005",
        balance=120000,
        is_verified=True
    ),
    User(
        name="Kavita Reddy",
        email="kavita.r@gmail.com",
        password="123",
        phone_no="9000111222",
        aadhaar_no="555566667777",
        bank_name="Canara Bank",
        account_no="10006",
        balance=28500,
        is_verified=False
    ),
    User(
        name="Arjun Malhotra",
        email="arjun.m@protonmail.com",
        password="123",
        phone_no="9555666777",
        aadhaar_no="666677778888",
        bank_name="Kotak Mahindra",
        account_no="10007",
        balance=95000,
        is_verified=True
    )

]

for user in users:

    db.add(user)

db.commit()

print("Dummy users inserted")