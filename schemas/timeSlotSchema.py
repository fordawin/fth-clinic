from datetime import datetime as dt
from datetime import time as t
from datetime import date as d
from pydantic import BaseModel
from typing import Optional

class TimeSlotBase(BaseModel):
    slot_capacity: Optional[str]
    slot_date: d

# Schema for request body
# class CreateUser(UserBase):
#     password: str

# # Schema for response body
# class User(UserBase):
#     created_at: dt
#     updated_at: dt

class TimeSlotUpdate(BaseModel):
    slot_capacity: Optional[str]
    slot_date: Optional[d]