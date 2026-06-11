from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import SessionLocal
from backend.transaction_models import Transaction
from datetime import datetime
from backend.bank_account_models import BankAccount

def get_user_analytics(email: str):

    db: Session = SessionLocal()

    active_account = db.query(
        BankAccount
    ).filter(
        BankAccount.user_email == email,
        BankAccount.is_active == True
    ).first()

    if not active_account:
        return {
            "total_sent": 0,
            "total_received": 0,
            "top_category": "None",
            "monthly_spending": 0
        }
    total_sent = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.sender_account_no ==
        active_account.account_no,

        Transaction.status ==
        "Sucessfull Transaction"
    ).scalar()

    total_received = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.receiver_account_no ==
        active_account.account_no,

        Transaction.status ==
        "Sucessfull Transaction"
    ).scalar()

    top_category_data = db.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter(
        Transaction.sender_account_no ==
        active_account.account_no,

        Transaction.status ==
        "Sucessfull Transaction"
    ).group_by(
        Transaction.category
    ).order_by(
        func.sum(Transaction.amount).desc()
    ).first()
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_spending = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.sender_account_no ==
        active_account.account_no,

        Transaction.status ==
        "Sucessfull Transaction",

        func.extract(
            "month",
            Transaction.created_at
        ) == current_month,

        func.extract(
            "year",
            Transaction.created_at
        ) == current_year
    ).scalar()

    db.close()

    return {
        "total_sent": total_sent or 0,
        "total_received": total_received or 0,
        "top_category": top_category_data[0] if top_category_data else "None",
        "monthly_spending": monthly_spending or 0
    }
