from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.auth import get_current_user
from db.table import Biometric, LinkedBank, User

router = APIRouter()

@router.post("/bank/link")
def link_bank(
    bank_name: str,
    account_number: str,
    ifsc: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    bank = LinkedBank(
        user_id=current_user.id,
        bank_name=bank_name,
        account_number=account_number,
        ifsc=ifsc
    )
    db.add(bank)
    db.commit()
    return {"message": "Bank linked successfully"}

@router.get("/bank/linked")
def get_linked_banks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    banks = db.query(LinkedBank).filter(LinkedBank.user_id == current_user.id).all()
    if not banks:
        raise HTTPException(status_code=404, detail="No linked banks found")
    return banks

@router.post("/biometric/register")
def register_biometric(biometric_hash: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bio = Biometric(
        user_id=current_user.id,
        biometric_hash=biometric_hash
    )
    db.add(bio)
    db.commit()
    return {"message": "Biometric registered successfully"}
