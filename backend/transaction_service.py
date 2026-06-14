from sqlalchemy.orm import Session
from backend.bank_account_models import BankAccount
from backend.transaction_models import Transaction
from backend.websocket_manager import manager
from backend.redis_cache import RedisCache
from backend.fraud_service import FraudService
from backend.redis_client import redis_client

cache = RedisCache()


class TransactionService:

    fraud = FraudService()

    async def send_money(self, data, db: Session):

        sender = db.query(BankAccount).filter(
            BankAccount.user_email == data.sender_email,
            BankAccount.is_active == True
        ).first()

        receiver = db.query(BankAccount).filter(
            BankAccount.user_email == data.receiver_email,
            BankAccount.is_active == True
        ).first()

        if not sender:
            return {"error": "sender account not found"}

        if not receiver:
            return {"error": "receiver account not found"}

        if sender.balance < data.amount:
            return {"error": "Insufficient balance"}

        risk_score = self.fraud.calculate_risk(sender, receiver, data.amount)

        if risk_score >= 70:
            await manager.send_personal_message(
                sender.user_email,
                f"🚨 Transaction BLOCKED due to risk score: {risk_score}"
            )
            return {
                "status": "blocked",
                "risk_score": risk_score
            }

        elif risk_score >= 40:
            await manager.send_personal_message(
                sender.user_email,
                f"⚠️ Warning: risk score {risk_score}"
            )

        sender.balance -= data.amount
        receiver.balance += data.amount

        txn = Transaction(
            sender_email=data.sender_email,
            receiver_email=data.receiver_email,

            sender_account_no=
            sender.account_no,

            receiver_account_no=
            receiver.account_no,

            amount=data.amount,
            category=data.category,
            status="Sucessfull Transaction",
            note=data.note
        )

        db.add(txn)
        db.commit()


        for key in redis_client.scan_iter("search:*"):
            redis_client.delete(key)

        cache.save_balance(sender.user_email, sender.balance)
        cache.save_balance(receiver.user_email, receiver.balance)

        await manager.send_personal_message(
            sender.user_email,
            f"₹{data.amount} sent to {receiver.user_email}"
        )

        await manager.send_personal_message(
            sender.user_email,
            f"Balance: {sender.balance}"
        )

        await manager.send_personal_message(
            receiver.user_email,
            f"₹{data.amount} received from {sender.user_email}"
        )

        await manager.send_personal_message(
            receiver.user_email,
            f"Balance: {receiver.balance}"
        )

        return {
            "message": "Transaction successful",
            "risk_score": risk_score
        }

    def get_history(self, email, db: Session):

        active_account = db.query(
            BankAccount
        ).filter(
            BankAccount.user_email == email,
            BankAccount.is_active == True
        ).first()

        if not active_account:
            return []

        history = db.query(
            Transaction
        ).filter(
            (
                    Transaction.sender_account_no ==
                    active_account.account_no
            ) |
            (
                    Transaction.receiver_account_no ==
                    active_account.account_no
            )
        ).all()

        return [
            {
                "sender_email": txn.sender_email,
                "receiver_email": txn.receiver_email,
                "amount": txn.amount,
                "category": txn.category,
                "status": txn.status,
                "note": txn.note,
            }
            for txn in history
        ]