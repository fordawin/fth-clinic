from datetime import datetime as dt
from datetime import date as d
from typing import Optional
from pydantic import BaseModel
from fastapi import Form

class employeeUpdate(BaseModel):
    em_pic : Optional[str]
    em_firstName : Optional[str]
    em_middleName : Optional[str]
    em_lastName : Optional[str]
    em_fullName : Optional[str] 
    em_houseNo : Optional[str]
    em_street : Optional[str]
    em_brgy : Optional[str]
    em_city : Optional[str]
    em_address : Optional[str]
    em_status : Optional[str]
    em_email : Optional[str]
    em_contactNo : Optional[str]

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