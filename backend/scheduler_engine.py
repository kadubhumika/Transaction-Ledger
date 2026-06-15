import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from backend.database import SessionLocal
from backend.models import ScheduledPayment
from backend.transaction_models import Transaction
from backend.websocket_manager import manager
from backend.bank_account_models import BankAccount

scheduler = AsyncIOScheduler()

def execute_scheduled_payments():
    db = SessionLocal()
    try:
        payments = db.query(ScheduledPayment).filter(
            ScheduledPayment.status == "pending"
        ).all()

        for payment in payments:
            if payment.scheduled_time <= datetime.now():
                sender = db.query(BankAccount).filter(
                    BankAccount.user_email == payment.sender_email,
                    BankAccount.is_active == True
                ).first()

                receiver = db.query(BankAccount).filter(
                    BankAccount.user_email == payment.receiver_email,
                    BankAccount.is_active == True
                ).first()

                if not sender or not receiver:
                    payment.status = "failed"
                    db.commit()
                    continue

                if sender.balance >= payment.amount:
                    sender.balance -= payment.amount
                    receiver.balance += payment.amount

                    txn = Transaction(
                        sender_email=payment.sender_email,
                        receiver_email=payment.receiver_email,
                        sender_account_no=sender.account_no,
                        receiver_account_no=receiver.account_no,
                        amount=payment.amount,
                        category=payment.category,
                        note=payment.note,
                        status="Sucessfull Transaction"
                    )

                    db.add(txn)
                    payment.status = "completed"
                    db.commit()

                    loop = asyncio.get_event_loop()
                    asyncio.run_coroutine_threadsafe(
                        manager.send_personal_message(
                            payment.sender_email,
                            f"Scheduled Payment Sent ₹{payment.amount} to {payment.receiver_email}"
                        ), loop
                    )
                    asyncio.run_coroutine_threadsafe(
                        manager.send_personal_message(
                            payment.receiver_email,
                            f"Received ₹{payment.amount} from {payment.sender_email}"
                        ), loop
                    )
                else:
                    payment.status = "failed"
                    db.commit()
    except Exception as e:
        print(f"Error in scheduler execution: {e}")
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

def execute_scheduled_payments():
    print("🔥 Scheduler Tick")
    db = SessionLocal()
