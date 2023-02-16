from datetime import datetime as dt
from datetime import date as d
from typing import Optional
from fastapi import UploadFile, Form, File
from pydantic import BaseModel

class ProductBase(BaseModel):
    product_name : Optional[str]
    product_description : Optional[str]
    product_price: Optional[int]
    product_quantity: Optional[int]
    product_discount: Optional[int]

    @classmethod
    def as_form(
        cls,
        product_name: str = Form(...),
        product_description: str = Form(...),
        product_price: str = Form(...),
        product_quantity: str = Form(...),
        product_discount: str = Form(...),
    ):
        return cls(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            product_quantity=product_quantity,
            product_discount=product_discount
        )
    
class Service(ProductBase):
    product_status: str
    product_created_at: dt
    product_updated_at: dt

class productUpdate(BaseModel):
    product_name : Optional[str]
    product_price: Optional[int]
    product_quantity: Optional[int]

class Discount(BaseModel):
    product_discount: Optional[int]

# class ProductUpload(BaseModel):
#     file : UploadFile

#     @classmethod
#     def as_form(
#         cls,
#         file: UploadFile = File(...)
  
#     ):
#         return cls(
#             file=file

#         )