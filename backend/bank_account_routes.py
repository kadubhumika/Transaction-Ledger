from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.bank_account_models import BankAccount
from sqlalchemy import func

router = APIRouter()

@router.post("/accounts/create")
def create_account(data: dict, db: Session = Depends(get_db)):
    existing = db.query(
        BankAccount
    ).filter(
        BankAccount.user_email == data["email"]
    ).first()

    account = BankAccount(
        user_email=data["email"],
        bank_name=data["bank_name"],
        account_no=data["account_no"],
        balance=data.get("balance", 0),
        is_active=False if existing else True
    )

    db.add(account)
    db.commit()

    return {"message": "Account created"}


@router.get("/accounts/{email}")
def get_accounts(email: str, db: Session = Depends(get_db)):
    accounts = db.query(BankAccount).filter(
        BankAccount.user_email == email
    ).all()
    return accounts


@router.post("/accounts/switch")
def switch_account(data: dict, db: Session = Depends(get_db)):
    if not data.get("email") or not data.get("account_no"):
        return {"error": "Invalid request"}

    db.query(BankAccount).filter(
        BankAccount.user_email == data["email"]
    ).update({"is_active": False})

    account = db.query(BankAccount).filter(
        BankAccount.account_no == data["account_no"],
        BankAccount.user_email == data["email"]
    ).first()

    if not account:
        return {"error": "Account not found"}

    account.is_active = True
    db.commit()

    # 🚀 FIXED THE CRASH HERE: Using standard redis client delete methods directly
    from backend.redis_client import redis_client
    redis_client.delete(f"profile:{data['email']}")
    redis_client.delete(f"analytics:{data['email']}")

    return {"message": "Active account switched"}


@router.get("/accounts/active/{email}")
def active_account(email: str, db: Session = Depends(get_db)):
    account = db.query(BankAccount).filter(
        BankAccount.user_email == email,
        BankAccount.is_active == True
    ).first()
    return account


@router.get("/accounts/summary/{email}")
def summary(email: str, db: Session = Depends(get_db)):
    total = db.query(
        func.sum(BankAccount.balance)
    ).filter(
        BankAccount.user_email == email
    ).scalar()
    return {"total_balance": total or 0}
