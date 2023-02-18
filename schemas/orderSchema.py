from datetime import datetime as dt
from datetime import date as d
from typing import Optional
from pydantic import BaseModel
from fastapi import Form

class OrderBase(BaseModel):
    order_quantity : Optional[int] | None = None
    order_productid : Optional[str] | None = None
    order_remarks : Optional[str] | None = None

# Schema for request body
class CreatePost(OrderBase):
    pass

#Schema for response body
class Order(OrderBase):
    order_created_at: dt
    order_updated_at: dt

class PaymentBase(BaseModel):
    order_payment : Optional[int]
    
    @classmethod
    def as_form(
        cls,
        order_payment : int = Form(...)
    ):
        return cls(
            order_payment = order_payment
        )
    class Config:
        orm_mode = True