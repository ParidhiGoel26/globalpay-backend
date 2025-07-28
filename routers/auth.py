from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from db.database import get_db
from db.table import User
from db.auth import register_user, verify_user, login_user, get_current_user, kyc

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=dict)
def register_route(phone_number: str, full_name: str, db: Session = Depends(get_db)):
    user = register_user(db, phone_number, full_name)
    return {"id": user.id, "phone_status": user.phone_status, "full_name": user.full_name}

@router.post("/verify", response_model=dict)
def verify_route(phone_number: str, otp: str, password: str, db: Session = Depends(get_db)):
    return verify_user(db, phone_number, otp, password)

@router.post("/login", response_model=TokenResponse)
def login_route(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user(db, form_data.username, form_data.password)

@router.post("/kyc", summary="Upload documents for KYC")
async def upload_kyc(
    sec_pin: int = Form(...),
    id_proof: Optional[UploadFile] = File(None),  # Optional upload
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return kyc(db, sec_pin, id_proof, current_user)

@router.get("/me")
def get_current_user_route(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "phone_number": current_user.phone_number,
        "full_name": current_user.full_name,
        "phone_status": current_user.phone_status,
        "kyc_status": current_user.kyc_status}