from pydantic import BaseModel

class SendMoneyData(BaseModel):

    sender_email: str

    receiver_email: str

    amount: int

    category: str

    note: str