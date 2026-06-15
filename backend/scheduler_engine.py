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
    print("🔥 Scheduler Tick")

    db = SessionLocal()

    try:
        payments = db.query(ScheduledPayment).filter(
            ScheduledPayment.status == "pending"
        ).all()

        print(f"Pending payments found: {len(payments)}")

        for payment in payments:

            print(
                f" Payment {payment.id} | "
                f"{payment.sender_email} -> {payment.receiver_email} | "
                f"{payment.amount} | "
                f"{payment.status} | "
                f"{payment.scheduled_time}"
            )

            if payment.scheduled_time <= datetime.now():

                print(f"Executing payment {payment.id}")

                sender = db.query(BankAccount).filter(
                    BankAccount.user_email == payment.sender_email,
                    BankAccount.is_active == True
                ).first()

                receiver = db.query(BankAccount).filter(
                    BankAccount.user_email == payment.receiver_email,
                    BankAccount.is_active == True
                ).first()

                print(f"Sender Account: {sender}")
                print(f"Receiver Account: {receiver}")

                if sender:
                    print(f"Sender Balance: {sender.balance}")

                if not sender or not receiver:
                    print(" Sender or Receiver not found")
                    payment.status = "failed"
                    db.commit()
                    continue

                if sender.balance >= payment.amount:

                    print(" Balance check passed")

                    sender.balance -= payment.amount
                    receiver.balance += payment.amount

                    print(
                        f"New Sender Balance: {sender.balance}"
                    )
                    print(
                        f"New Receiver Balance: {receiver.balance}"
                    )

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

                    print(
                        f" Payment {payment.id} completed"
                    )

                else:
                    print(
                        f" Insufficient Balance. "
                        f"Have={sender.balance}, Need={payment.amount}"
                    )

                    payment.status = "failed"
                    db.commit()

    except Exception as e:
        print(f" Scheduler Error: {e}")

    finally:
        db.close()