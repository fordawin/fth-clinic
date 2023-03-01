from datetime import datetime as dt
from datetime import time as t
from datetime import date as d
from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class TimeSlotBase(BaseModel):
    slot_capacity: Optional[str]
    slot_date: d

class TimeSlotUpdate(BaseModel):
    slot_start : Optional[t]
    slot_end : Optional[t]
    slot_capacity: Optional[str]
    slot_date: Optional[d]
    slot_status: Optional[str]

class SlotBase(BaseModel):
    slot_number : Optional[int]
    slot_duration : Optional[t]
    slot_capacity: Optional[str]
    slot_daystart: Optional[str]
    slot_date: Optional[d]

class Date(BaseModel):
    slot_date: str

    @classmethod
    def as_form(
        cls,
        slot_date : str = Form(...),
    ):
        return cls(
            slot_date = slot_date,
        )
    class Config:
        orm_mode = True