from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid
import datetime

from db.table import Wallet, Transaction, TransactionType, TransactionStatus

def create_transaction(
    db: Session,
    sender_wallet_id: str,
    amount: float,
    type: TransactionType,
    recipient_wallet_id: str = None,
) -> Transaction:
    sender_wallet = db.query(Wallet).filter(Wallet.id == sender_wallet_id).first()
    recipient_wallet = db.query(Wallet).filter(Wallet.id == recipient_wallet_id).first()
    # For deposit or refund, sender is None or system account
    if type in [TransactionType.deposit, TransactionType.refund]:
        if recipient_wallet:
            recipient_wallet.balance += amount

    # For withdrawal or payment, deduct from sender
    elif type == TransactionType.payment:
        if not sender_wallet:
            raise HTTPException(status_code=404, detail="Sender wallet not found")
        if not recipient_wallet:
            raise HTTPException(status_code=404, detail="Recipient wallet not found")
        
        if sender_wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        sender_wallet.balance -= amount
        recipient_wallet.balance += amount

    elif type == TransactionType.withdrawal:
        if not sender_wallet:
            raise HTTPException(status_code=404, detail="Sender wallet not found")
        if sender_wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        sender_wallet.balance -= amount

    elif type == TransactionType.offline_sync:
        pass

    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    transaction = Transaction(
        id=str(uuid.uuid4()),
        sender_wallet_id=sender_wallet_id,
        reciepient_wallet_id=recipient_wallet_id,
        amount=amount,
        type=type,
        status=TransactionStatus.success,
        timestamp=datetime.datetime.utcnow(),
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_wallet_balance(db: Session, user_id: str) -> float:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet.balance
