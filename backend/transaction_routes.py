from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.transaction_data import SendMoneyData

from backend.transaction_service import TransactionService

router = APIRouter()

service = TransactionService()

@router.post("/send-money")
async def send_money(
    data: SendMoneyData,
    db: Session = Depends(get_db)
):

    return await service.send_money(data, db)

@router.get("/history/{email}")

def get_history(
    email: str,
    db: Session = Depends(get_db)
):

    return service.get_history(
        email,
        db
    )