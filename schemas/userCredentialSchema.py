from datetime import datetime as dt
from datetime import date as d
from typing import Optional, List
from pydantic import BaseModel
from fastapi import Request, Form

class UserBase(BaseModel):
    user_email: Optional[str]
    user_username: Optional[str]
    user_password: Optional[str]
    # user_created_by: str
    # user_updated_by: str

    class Config:
        orm_mode = True

# class LoginForm:
#     def __init__(self, request: Request):
#         self.request: Request = request
#         self.errors: List = []
#         self.username: Optional[str] = None
#         self.password: Optional[str] = None

#     async def load_data(self):
#         form = await self.request.form()
#         self.username = form.get(
#             "email"
#         )  # since outh works on username field we are considering email as username
#         self.password = form.get("password")

#     async def is_valid(self):
#         if not self.password or not len(self.password) >= 4:
#             self.errors.append("A valid password is required")
#         if not self.errors:
#             return True
#         return False

class LoginForm(BaseModel):
    user_email: Optional[str]
    user_password: Optional[str]

    @classmethod
    def as_form(
        cls,
        user_email: str = Form(...),
        user_password: str = Form(...)
    ):
        return cls(
            user_email = user_email,
            user_password = user_password
        )
    class Config:
        orm_mode: True

class TokenData(BaseModel):
    id : str
    email: str
    type: str


class UserRead(UserBase):
    user_id: str

class AdminBase(BaseModel):
    ad_user_credential: str

    class Config:
        orm_mode = True

class ClientBase(UserBase):
    cl_pic : Optional[str]
    cl_firstName : Optional[str]
    cl_middleName : Optional[str]
    cl_lastName : Optional[str]
    cl_fullName : Optional[str]
    cl_houseNo : Optional[str]
    cl_street : Optional[str]
    cl_brgy : Optional[str]
    cl_city : Optional[str]
    cl_address : Optional[str]
    cl_status : Optional[str]
    cl_maritalStatus : Optional[str]
    cl_birthdate : Optional[d]
    cl_gender : Optional[str]
    cl_contactNo : Optional[str]
    cl_user_credential : Optional[str]
    # cl_created_by : str
    # cl_updated_by : str

    @classmethod
    def as_form(
        cls,
        user_email: str = Form(...),
        user_username: str = Form(...),
        user_password: str = Form(...),
        cl_firstName : str = Form(...),
        cl_middleName : str = Form(""),
        cl_lastName : str = Form(...),
        cl_houseNo : str = Form(...),
        cl_street : str = Form(...),
        cl_brgy : str = Form(...),
        cl_city : str = Form(...),
        cl_maritalStatus : str = Form(...),
        cl_birthdate : d = Form(...),
        cl_gender : str = Form(...),
        cl_contactNo : str = Form(...)
    ):
        return cls(
            user_email = user_email,
            user_username = user_username,
            user_password = user_password,
            cl_firstName = cl_firstName,
            cl_middleName = cl_middleName,
            cl_lastName = cl_lastName,
            cl_fullName = cl_firstName + cl_middleName + cl_lastName,
            cl_houseNo = cl_houseNo,
            cl_street = cl_street,
            cl_brgy = cl_brgy,
            cl_city = cl_city,
            cl_address = cl_houseNo + cl_street + cl_brgy + cl_city,
            cl_maritalStatus = cl_maritalStatus,
            cl_birthdate = cl_birthdate,
            cl_gender = cl_gender,
            cl_contactNo = cl_contactNo,
        )
    class Config:
        orm_mode = True

class EmployeeBase(UserBase):
    em_id : Optional[str] = None
    em_pic : Optional[str] = None
    em_firstName : Optional[str] = None
    em_middleName : Optional[str] = None 
    em_lastName : Optional[str] = None
    em_fullName : Optional[str] = None
    em_houseNo : Optional[str] = None
    em_street : Optional[str] = None
    em_brgy : Optional[str] = None
    em_city : Optional[str] = None
    em_address : Optional[str] = None
    em_status : Optional[str] = None
    em_contactNo : Optional[str] = None
    # em_created_by : str
    # em_updated_by : str

    @classmethod
    def as_form(
        cls,
        user_email: str = Form(...),
        user_username: str = Form(...),
        user_password: str = Form(...),
        em_firstName : str = Form(...),
        em_middleName : str = Form(""),
        em_lastName : str = Form(...),
        em_houseNo : str = Form(...),
        em_street : str = Form(...),
        em_brgy : str = Form(...),
        em_city : str = Form(...),
        em_birthdate : d = Form(...),
        em_contactNo : str = Form(...)
    ):
        return cls(
            user_email = user_email,
            user_username = user_username,
            user_password = user_password,
            em_firstName = em_firstName,
            em_middleName = em_middleName,
            em_lastName = em_lastName,
            em_fullName = em_firstName + em_middleName + em_lastName,
            em_houseNo = em_houseNo,
            em_street = em_street,
            em_brgy = em_brgy,
            em_city = em_city,
            em_address = em_houseNo + em_street + em_brgy + em_city,
            em_birthdate = em_birthdate,
            em_contactNo = em_contactNo,
        )
    class Config:
        orm_mode = True

class DoctorBase(UserBase):
    dt_pic : Optional[str] = None 
    dt_firstName : Optional[str] = None 
    dt_middleName : Optional[str] = None 
    dt_lastName : Optional[str] = None 
    dt_fullName : Optional[str] = None 
    dt_houseNo : Optional[str] = None 
    dt_street : Optional[str] = None 
    dt_brgy : Optional[str] = None 
    dt_city : Optional[str] = None 
    dt_address : Optional[str] = None 
    dt_status : Optional[str] = None 
    dt_contactNo : Optional[str] = None 
    # dt_created_by: str
    # dt_updated_by: str
    @classmethod
    def as_form(
        cls,
        user_email: str = Form(...),
        user_username: str = Form(...),
        user_password: str = Form(...),
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
            user_email = user_email,
            user_username = user_username,
            user_password = user_password,
            dt_firstName = dt_firstName,
            dt_middleName = dt_middleName,
            dt_lastName = dt_lastName,
            dt_fullName = dt_firstName + dt_middleName + dt_lastName,
            dt_houseNo = dt_houseNo,
            dt_street = dt_street,
            dt_brgy = dt_brgy,
            dt_city = dt_city,
            dt_address = dt_houseNo + dt_street + dt_brgy + dt_city,
            dt_contactNo = dt_contactNo,
        )
    class Config:
        orm_mode = True

# Schema for response body
class User(UserBase):
    user_type: str
    user_created_at: dt
    user_updated_at: dt

    class Config:
        orm_mode = True

class Client(ClientBase):
    cl_created_at: dt
    cl_updated_at: dt

    class Config:
        orm_mode = True

class Employee(EmployeeBase):
    em_created_at: dt
    em_updated_at: dt

    class Config:
        orm_mode = True

class Doctor(DoctorBase):
    dt_created_at: dt
    dt_updated_at: dt

    class Config:
        orm_mode = True

class updateUser(BaseModel):
    user_username: Optional[str] | None = None
    user_password: Optional[str] | None = None
    old_password: Optional[str] | None = None
    user_passwordre: Optional[str] | None = None
    user_email: Optional[str] | None = None

    @classmethod
    def as_form(
        cls,
        old_password: str = Form(...),
        user_password: str = Form(...),
        user_passwordre: str = Form(...)
    ):
        return cls(
            old_password = old_password,
            user_password = user_password,
            user_passwordre = user_passwordre
        )
    class Config:
        orm_mode = True


