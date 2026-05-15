from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import SessionLocal
from backend.transaction_models import Transaction
from datetime import datetime

def get_user_analytics(email: str):
    db:Session=SessionLocal()
    total_sent = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.sender_email == email
    ).scalar()

    total_received = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.receiver_email == email
    ).scalar()

    top_category_data = db.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter(
        Transaction.sender_email == email
    ).group_by(
        Transaction.category
    ).order_by(
        func.sum(Transaction.amount).desc()
    ).first()

    current_month = datetime.now().month

    monthly_spending = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.sender_email == email
    ).filter(
        func.extract(
            "month",
            Transaction.created_at
        ) == current_month
    ).scalar()

    db.close()

    return {

        "total_sent":
            total_sent or 0,

        "total_received":
            total_received or 0,

        "top_category":
            top_category_data[0]
            if top_category_data
            else "None",

        "monthly_spending":
            monthly_spending or 0

    }