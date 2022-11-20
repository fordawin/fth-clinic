from datetime import datetime as dt
from datetime import date as d
from typing import Optional
from pydantic import BaseModel
from fastapi import Form

class employeeUpdate(BaseModel):
    em_pic : Optional[str] | None = None
    em_firstName : Optional[str] | None = None
    em_middleName : Optional[str] | None = None
    em_lastName : Optional[str] | None = None
    em_fullName : Optional[str] | None = None
    em_houseNo : Optional[str] | None = None
    em_street : Optional[str] | None = None
    em_brgy : Optional[str] | None = None
    em_city : Optional[str] | None = None
    em_address : Optional[str] | None = None
    em_status : Optional[str] | None = None
    em_email : Optional[str] | None = None
    em_contactNo : Optional[str] | None = None

    @classmethod
    def as_form(
        cls,
        em_firstName : str = Form(...),
        em_middleName : str = Form(""),
        em_lastName : str = Form(...),
        em_houseNo : str = Form(...),
        em_street : str = Form(...),
        em_brgy : str = Form(...),
        em_city : str = Form(...),
        em_contactNo : str = Form(...),
    ):
        return cls(
            em_firstName = em_firstName,
            em_middleName = em_middleName,
            em_lastName = em_lastName,
            em_fullName = em_firstName + " " + em_middleName + " " + em_lastName,
            em_houseNo = em_houseNo,
            em_street = em_street,
            em_brgy = em_brgy,
            em_city = em_city,
            em_address = em_houseNo + " " + em_street + " " + em_brgy + " " + em_city,
            em_contactNo = em_contactNo,
        )
    class Config:
        orm_mode = True