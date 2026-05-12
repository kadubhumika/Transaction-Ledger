from pydantic import BaseModel


class UpdateProfileData(BaseModel):

    name: str

    phone_no: str

    bank_name: str


class AddBalanceData(BaseModel):

    email: str

    amount: int