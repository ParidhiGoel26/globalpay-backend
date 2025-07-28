from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
import uuid

from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from db.table import User, Wallet, PhoneStatus, KYCStatus
from db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT config

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user

def register_user(db: Session, phone_number: str, full_name: str) -> User:
    existing = db.query(User).filter(User.phone_number == phone_number).first()
    if existing:
        if existing.phone_status != PhoneStatus.verified:
            # Delete the unverified user to allow re-registration
            db.delete(existing)
            db.commit()
        else:
            raise HTTPException(status_code=400, detail="Phone number already registered and verified")
    
    user = User(
        id=str(uuid.uuid4()),
        phone_number=phone_number,
        full_name=full_name,
        phone_status=PhoneStatus.pending,
        password_hash="",  # to be set on verify
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def verify_user(db: Session, phone_number: str, otp: str, password: str):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # OTP always "123456" for mock
    if otp != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP")
    user.phone_status = PhoneStatus.verified
    user.password_hash = hash_password(password)
    db.commit()

    return {"message": "Phone verified and password set"}

def login_user(db: Session, phone_number: str, password: str):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=404, detail="User not found or not verified")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def kyc(db:Session, sec_pin: int, id_proof: Optional[UploadFile] = None, user: User = Depends(get_current_user)):
    if sec_pin != 123456:
        user.kyc_status = KYCStatus.pending
        db.commit()
        raise HTTPException(status_code=400, detail="KYC failed")

    user.kyc_status = KYCStatus.verified
    wallet = Wallet(
        id=user.phone_number,
        user_id=user.id
        )
    db.add(wallet)
    db.commit()
    return {"message": "KYC verified"}
