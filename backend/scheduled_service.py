from backend.database import SessionLocal

from backend.models import ScheduledPayment

def create_scheduled_payment(data):

    db = SessionLocal()

    payment = ScheduledPayment(

        sender_email=data.sender_email,

        receiver_email=data.receiver_email,

        amount=data.amount,

        category=data.category,

        note=data.note,

        scheduled_time=
        f"{data.scheduled_date} {data.scheduled_time}"
    )

    db.add(payment)

    db.commit()

    return {
        "message":"Payment Scheduled Successfully"
    }