from datetime import datetime as dt
from datetime import date as d
from typing import Optional, List
from pydantic import BaseModel
from fastapi import Request, Form

class ServiceBase(BaseModel):
    service_name : Optional[str] | None = None
    service_price : Optional[str] | None = None
    service_description : Optional[str] | None = None

class ServiceBas(ServiceBase):
    service_status: Optional[str] | None = None
    # service_created_at: dt
    # service_updated_at: dt

    @classmethod
    def as_form(
        cls,
        service_name: str = Form(...),
        service_price: int = Form(...),
        service_description: str = Form(...),
        service_status: str = Form(...),
    ):
        return cls(
            service_name = service_name,
            service_price = service_price,
            service_description = service_description,
            service_status = service_status
        )
    class Config:
        orm_mode = True

class updateService(BaseModel):
    service_name : Optional[str]
    service_description: Optional[str]
    service_price: Optional[int]
    service_status: Optional[str]