from datetime import datetime as dt
from datetime import date as d
from typing import Optional
from pydantic import BaseModel, validator, ValidationError
from fastapi import Form

class doctorUpdate(BaseModel):
    dt_pic : Optional[str]
    dt_firstName : Optional[str]
    dt_middleName : Optional[str]
    dt_lastName : Optional[str]
    dt_fullName : Optional[str]
    dt_houseNo : Optional[str]
    dt_street : Optional[str]
    dt_brgy : Optional[str]
    dt_city : Optional[str]
    dt_address : Optional[str]
    dt_status : Optional[str]
    dt_contactNo : Optional[str]
    dt_user_credential: Optional[str]

    @classmethod
    def as_form(
        cls,
        dt_pic : str = Form(...),
        dt_firstName : str = Form(...),
        dt_middleName : str = Form(...),
        dt_lastName : str = Form(...),
        # dt_fullName : str = Form(...),
        dt_houseNo : str = Form(...),
        # dt_address : str = Form(...),
        dt_street : str = Form(...),
        dt_brgy : str = Form(...),
        dt_city : str = Form(...),
        dt_contactNo : str = Form(...),
        dt_status : str = Form(...),
    ):
        return cls(
            dt_pic = dt_pic,
            dt_firstName = dt_firstName,
            dt_middleName = dt_middleName,
            dt_lastName = dt_lastName,
            dt_fullName = dt_firstName + dt_middleName + dt_lastName,
            dt_houseNo = dt_houseNo,
            dt_street = dt_street,
            cl_address = dt_houseNo + dt_street + dt_brgy + dt_city,
            dt_status = dt_status,
            dt_brgy = dt_brgy,
            dt_city = dt_city,
            dt_contactNo = dt_contactNo,
            # dt_user_credential = dt_user_credential
        )

    class Config:
        orm_mode = True