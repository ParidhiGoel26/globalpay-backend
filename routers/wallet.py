from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db
from db.auth import get_current_user
from db.table import Wallet, Transaction, TransactionType, User
from db.wallet import create_transaction

router = APIRouter()

# class PayRecipient(BaseModel):
#     phone: str  # recipient's phone (i.e., wallet id)


@router.get("/")
def get_wallet_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.id == current_user.phone_number).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.post("/load")
def load_wallet(amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet_id = current_user.phone_number
    create_transaction(
        db=db,
        sender_wallet_id=None,
        recipient_wallet_id=wallet_id,
        amount=amount,
        type=TransactionType.deposit
    )

    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    return wallet


@router.post("/pay")
def pay(
    recipient: str, amount: float, otp: str,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if otp != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP")

    transaction = create_transaction(
        db=db,
        sender_wallet_id=current_user.phone_number,
        recipient_wallet_id=recipient,
        amount=amount,
        type=TransactionType.payment
    )

    return transaction


@router.post("/withdraw")
def withdraw(amount: float, otp: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if otp != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP")

    transaction = create_transaction(
        db=db,
        sender_wallet_id=current_user.phone_number,
        recipient_wallet_id=None,
        amount=amount,
        type=TransactionType.withdrawal
    )

    return transaction


@router.post("/transactions")
def list_transactions(filter: TransactionType = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet_id = current_user.phone_number

    query = db.query(Transaction).filter(
        (Transaction.sender_wallet_id == wallet_id) |
        (Transaction.reciepient_wallet_id == wallet_id)
    )

    if filter:
        query = query.filter(Transaction.type == filter)

    return query.order_by(Transaction.timestamp.desc()).all()
