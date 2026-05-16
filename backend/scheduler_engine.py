from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime

from backend.database import SessionLocal

from backend.models import ScheduledPayment
from backend.models import User
from backend.transaction_models import Transaction

from backend.websocket_manager import manager

scheduler = AsyncIOScheduler()

async def execute_scheduled_payments():

    db = SessionLocal()

    try:

        payments = db.query(
            ScheduledPayment
        ).filter(

            ScheduledPayment.status == "pending"

        ).all()

        for payment in payments:

            if payment.scheduled_time <= datetime.now():

                sender = db.query(User).filter(
                    User.email == payment.sender_email
                ).first()

                receiver = db.query(User).filter(
                    User.email == payment.receiver_email
                ).first()

                if sender.balance >= payment.amount:

                    sender.balance -= payment.amount

                    receiver.balance += payment.amount

                    txn = Transaction(

                        sender_email=payment.sender_email,

                        receiver_email=payment.receiver_email,

                        amount=payment.amount,

                        category=payment.category,

                        note=payment.note,

                        status="scheduled-success"
                    )

                    db.add(txn)

                    payment.status = "completed"

                    db.commit()

                    await manager.send_personal_message(

                        payment.sender_email,

                        f"Scheduled Payment Sent ₹{payment.amount} to {payment.receiver_email}"
                    )

                    await manager.send_personal_message(

                        payment.receiver_email,

                        f"Received ₹{payment.amount} from {payment.sender_email}"
                    )

                else:

                    payment.status = "failed"

                    db.commit()

    finally:

        db.close()

async def start_scheduler():

    scheduler.add_job(

        execute_scheduled_payments,

        "interval",

        seconds=10
    )

    scheduler.start()

    print("Scheduler started successfully!")