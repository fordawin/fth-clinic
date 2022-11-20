from datetime import datetime as dt
from datetime import date as d
from typing import Optional
from pydantic import BaseModel
from fastapi import Form

class doctorUpdate(BaseModel):
    dt_pic : Optional[str] | None = None
    dt_firstName : Optional[str] | None = None
    dt_middleName : Optional[str] | None = None
    dt_lastName : Optional[str] | None = None
    dt_fullName : Optional[str] | None = None
    dt_houseNo : Optional[str] | None = None
    dt_street : Optional[str] | None = None
    dt_brgy : Optional[str] | None = None
    dt_city : Optional[str] | None = None
    dt_address : Optional[str] | None = None
    dt_status : Optional[str] | None = None
    dt_contactNo : Optional[str] | None = None
    dt_user_credential: Optional[str] | None = None

    @classmethod
    def as_form(
        cls,
        dt_firstName : str = Form(...),
        dt_middleName : str = Form(""),
        dt_lastName : str = Form(...),
        dt_houseNo : str = Form(...),
        dt_street : str = Form(...),
        dt_brgy : str = Form(...),
        dt_city : str = Form(...),
        dt_contactNo : str = Form(...),
    ):
        return cls(
            dt_firstName = dt_firstName,
            dt_middleName = dt_middleName,
            dt_lastName = dt_lastName,
            dt_houseNo = dt_houseNo,
            dt_street = dt_street,
            dt_brgy = dt_brgy,
            dt_city = dt_city,
            dt_contactNo = dt_contactNo,
        )

    class Config:
        orm_mode = True