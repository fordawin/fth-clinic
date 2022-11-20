from datetime import datetime as dt
from datetime import time as t
from datetime import date as d
from pydantic import BaseModel
from fastapi import Form
from typing import Optional
from schemas.userCredentialSchema import UserBase

class PrescriptionBase(BaseModel):
    presc_appointmentID : str
    presc_medication : str
    presc_treatment : str
    presc_remarks : str

    @classmethod
    def as_form(
        cls,
        presc_appointmentID : str = Form(...),
        presc_medication : str = Form(...),
        presc_treatment : str = Form(...),
        presc_remarks : str = Form(...)
    ):
        return cls(
            presc_appointmentID = presc_appointmentID,
            presc_medication = presc_medication,
            presc_treatment = presc_treatment,
            presc_remarks = presc_remarks
        )
    class Config:
        orm_mode = True

# Schema for response body
class User(PrescriptionBase):
    presc_created_at: dt
    presc_updated_at: dt


class PrescriptionUpdate(UserBase):
    presc_appointmentID : Optional[str]
    presc_medication : Optional[str]
    presc_treatment : Optional[str]
    presc_remarks : Optional[str]