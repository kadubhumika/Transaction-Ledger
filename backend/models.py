from sqlalchemy import Column, Integer, String, Boolean, Float

from backend.database import Base
from sqlalchemy import DateTime


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String, unique=True)

    password = Column(String)

    phone_no = Column(String)

    aadhaar_no = Column(String)

    bank_name = Column(String)

    account_no = Column(String,unique=True)

    balance = Column(Integer, default=10000)

    is_verified = Column(Boolean, default=False)

class ScheduledPayment(Base):

    __tablename__ = "scheduled_payments"

    id = Column(Integer, primary_key=True)

    sender_email = Column(String)

    receiver_email = Column(String)

    amount = Column(Float)

    category = Column(String)

    note = Column(String)

    scheduled_time = Column(DateTime)

    status = Column(String, default="pending")