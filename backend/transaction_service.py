from sqlalchemy.orm import Session

from backend.models import User

from backend.transaction_models import Transaction

from backend.websocket_manager import manager

from backend.redis_cache import RedisCache

cache = RedisCache()
class TransactionService:
    async def send_money(self,data, db: Session):
        sender = db.query(User).filter(
            User.email == data.sender_email
        ).first()

        receiver = db.query(User).filter(
            User.email == data.receiver_email
        ).first()
        if not sender:
            return {"error": "sender_email not found"}
        if not receiver:
            return {"error": "receiver_email not found"}
        if sender.balance < data.amount:
            return {"error": "Insufficient balance"}

        sender.balance -= data.amount
        receiver.balance += data.amount
        txn = Transaction(
            sender_email = data.sender_email,
            receiver_email = data.receiver_email,
            amount= data.amount,
            category = data.category,
            status = "Sucessfull Transaction",
            note = data.note
        )
        db.add(txn)
        db.commit()
        cache.save_balance(
            sender.email,
            sender.balance
        )

        cache.save_balance(
            receiver.email,
            receiver.balance
        )
        await manager.send_message(
            sender.email,
            f"₹{data.amount} sent to {receiver.name}"
        )
        await manager.send_message(
            sender.email,
            f"After transaction cuurent balance is {sender.balance}"
        )

        # websocket receiver
        await manager.send_message(
            receiver.email,
            f"₹{data.amount} received from {sender.name}"
        )
        await manager.send_message(
            receiver.email,
            f"After transaction cuurent balance is{receiver.balance}"
        )
        return{
            "message": "Transaction successfull!!",
        }

    def get_history(self,email, db: Session):
        history = db.query(Transaction).filter(
            (Transaction.sender_email == email) | (Transaction.receiver_email == email)
        ).all()
        result = []
        for txn in history:
            result.append({
                "sender_email": txn.sender_email,
                "receiver_email": txn.receiver_email,
                "amount": txn.amount,
                "category": txn.category,
                "status": txn.status,
                "note": txn.note,
            })
        return result



