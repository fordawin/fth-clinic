from datetime import datetime as dt
from datetime import date as d
from typing import Optional
from pydantic import BaseModel
from fastapi import Form

class clientUpdate(BaseModel):
    cl_pic : Optional[str] = ...
    cl_firstName : Optional[str] = ...
    cl_middleName : Optional[str] = ...
    cl_lastName : Optional[str] = ...
    cl_fullName : Optional[str] = ...
    cl_houseNo : Optional[str] = ...
    cl_street : Optional[str] = ...
    cl_brgy : Optional[str] = ...
    cl_city : Optional[str] = ...
    cl_maritalStatus : Optional[str] = ...
    cl_validId : Optional[str] = ...
    cl_validIdNumber : Optional[str] = ...
    cl_contactNo : Optional[str] = ...

    @classmethod
    def as_form(
        cls,
        cl_firstName : Optional[str] = Form(...),
        cl_middleName : Optional[str] = Form(...),
        cl_lastName : Optional[str] = Form(...),
        cl_houseNo : Optional[str] = Form(...),
        cl_street : Optional[str] = Form(...),
        cl_brgy : Optional[str] = Form(...),
        cl_city : Optional[str] = Form(...),
        cl_maritalStatus : Optional[str] = Form(...),
        cl_contactNo : Optional[str] = Form(...),
    ):
        return cls(
            cl_firstName = cl_firstName,
            cl_middleName = cl_middleName,
            cl_lastName = cl_lastName,
            # cl_fullName = cl_firstName + " " + cl_middleName + " " + cl_lastName,
            cl_houseNo = cl_houseNo,
            cl_street = cl_street,
            cl_brgy = cl_brgy,
            cl_city = cl_city,
            # cl_address = cl_houseNo + cl_street + cl_brgy + cl_city,
            cl_maritalStatus = cl_maritalStatus,
            cl_contactNo = cl_contactNo,
        )
    class Config:
        orm_mode = True