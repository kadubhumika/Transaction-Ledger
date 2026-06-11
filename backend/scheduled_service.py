from backend.database import SessionLocal

from backend.models import ScheduledPayment

from datetime import datetime
def create_scheduled_payment(data):
    scheduled_datetime = datetime.strptime(
        f"{data.scheduled_date} {data.scheduled_time}",
        "%Y-%m-%d %H:%M"
    )

    db = SessionLocal()

    try:

        payment = ScheduledPayment(
            sender_email=data.sender_email,
            receiver_email=data.receiver_email,
            amount=data.amount,
            category=data.category,
            note=data.note,
            scheduled_time=scheduled_datetime,
            status="pending"  # <-- Added missing status init
        )

        db.add(payment)
        db.commit()

        return {
            "message":"Payment Scheduled Successfully"
        }

    finally:
        db.close()