from datetime import datetime as dt
from datetime import time as t
from datetime import date as d
from pydantic import BaseModel
from typing import Optional

class TimeSlotBase(BaseModel):
    slot_capacity: Optional[str]
    slot_date: d

class TimeSlotUpdate(BaseModel):
    slot_capacity: Optional[str]
    slot_date: Optional[d]

class SlotBase(BaseModel):
    slot_number : Optional[int]
    slot_duration : Optional[t]
    slot_capacity: Optional[str]
    slot_daystart: Optional[str]
    slot_date: Optional[d]