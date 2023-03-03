from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from schemas.receiptSchema import ReceiptBase
from models.receiptModel import Receipt
from database import get_db
from dependencies import get_token
from systemlogs import *

router = APIRouter(
    prefix='/receipt',
    tags=['receipt']
)

@router.post('/')
def store(user: ReceiptBase, db: Session = Depends(get_db)):
    to_store = Receipt(
        receipt_appointmentID = user.receipt_appointmentID,
        receipt_clientID = user.receipt_clientID,
        receipt_amount = user.receipt_amount,
    )
    db.add(to_store)
    db.commit()
    return {'message': 'User stored successfully.'}


