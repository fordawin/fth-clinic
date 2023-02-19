from datetime import datetime as dt
from datetime import time as t
from datetime import date as d
from typing import Optional
from pydantic import BaseModel
from fastapi import Request, Form

class PaymentBase(BaseModel):
    payment_mode : Optional[str]
    payment_amount : Optional[str]
    payment_appointmentID : Optional[str]
    payment_points : Optional[str]
    
    @classmethod
    def as_form(
        cls,
        payment_mode : str = Form(...),
        payment_amount : str = Form(...),
        payment_appointmentID : str = Form(...)
    ):
        return cls(
            payment_mode = payment_mode,
            payment_amount = payment_amount,
            payment_appointmentID = payment_appointmentID
        )
    class Config:
        orm_mode = True

# Schema for response body
class User(PaymentBase):
    payment_created_at: dt
    payment_updated_at: dt

class PaymentUpdate(BaseModel):
    payment_mode : Optional[str]
    payment_amount : Optional[str]
    payment_appointmentID : Optional[str]
