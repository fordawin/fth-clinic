from datetime import datetime as dt
from datetime import time as t
from datetime import date as d
from pydantic import BaseModel
from fastapi import Request, Form
from typing import Optional, List


class AppointmentBase(BaseModel):
    ap_startTime : Optional[t]
    ap_date : Optional[d]
    ap_type : Optional[str]
    ap_service : Optional[str]
    ap_comorbidity : str
    ap_serviceType : str
    ap_slotID : str
    
    @classmethod
    def as_form(
        cls,
        ap_comorbidity : str = Form(...),
        ap_serviceType : str = Form(...),
        ap_slotID : str = Form(...)
    ):
        return cls(
            ap_comorbidity = ap_comorbidity,
            ap_serviceType = ap_serviceType,
            ap_slotID = ap_slotID
        )
    class Config:
        orm_mode = True

# Schema for request body
# class CreateUser(UserBase):
#     password: str

# Schema for response body
class Appointment(AppointmentBase):
    ap_created_at : dt
    ap_updated_at : dt

class AppointmentUpdate(BaseModel):
    ap_startTime : Optional[t]
    ap_date : Optional[d]
    ap_type : Optional[str]
    ap_service : Optional[str]
    ap_comorbidity : Optional[str]
    ap_serviceType : Optional[str]
    ap_slotID : Optional[str]

class AppointmentEmployee(BaseModel):
    ap_startTime : Optional[t]
    ap_date : Optional[d]
    ap_type : Optional[str]
    ap_clientID : Optional[str]
    ap_service : Optional[str]
    ap_comorbidity : str
    ap_serviceType : str
    ap_slotID : str