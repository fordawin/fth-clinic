from datetime import datetime as dt
from datetime import time as t
from datetime import date as d
from pydantic import BaseModel

class ReceiptBase(BaseModel):
    receipt_appointmentID : str
    receipt_clientID : str
    receipt_amount : str

# Schema for response body
class User(ReceiptBase):
    receipt_created_at: dt
    receipt_updated_at: dt