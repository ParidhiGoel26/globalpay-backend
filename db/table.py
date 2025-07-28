from sqlalchemy import Column, String, Float, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
import enum
import uuid
import datetime

class PhoneStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"

class KYCStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class TransactionType(str, enum.Enum):
    deposit = "deposit"
    payment = "payment"
    withdrawal = "withdrawal"
    refund = "refund"
    offline_sync = "offline_sync"

class TransactionStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone_status = Column(Enum(PhoneStatus), default="pending")
    kyc_status = Column(Enum(KYCStatus), default="pending")
    password_hash = Column(String)

    wallet = relationship("Wallet", back_populates="user", uselist=False)


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    balance = Column(Float, default=0.0)

    user = relationship("User", back_populates="wallet")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_wallet_id = Column(String, ForeignKey("wallets.id"), nullable=True)
    reciepient_wallet_id = Column(String, ForeignKey("wallets.id"), nullable=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default="pending")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class LinkedBank(Base):
    __tablename__ = "linked_banks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    bank_name = Column(String)
    account_number = Column(String)
    ifsc = Column(String)

class Biometric(Base):
    __tablename__ = "biometrics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    biometric_hash = Column(String)  # hashed fingerprint, palm scan etc.
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)