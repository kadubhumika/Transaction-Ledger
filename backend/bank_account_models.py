from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from backend.database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)

    user_email = Column(String, index=True)

    bank_name = Column(String)   # RBI / SBI / HDFC

    account_no = Column(String, unique=True)

    balance = Column(Integer, default=0)

    is_active = Column(Boolean, default=False)