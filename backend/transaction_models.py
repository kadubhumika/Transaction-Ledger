from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    sender_email = Column(String)
    receiver_email = Column(String)
    amount = Column(Integer)
    category = Column(String)
    status = Column(String)
    note = Column(String)