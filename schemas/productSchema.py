from datetime import datetime as dt
from datetime import date as d
from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    product_name : Optional[str]
    product_description : Optional[str]
    product_price: Optional[int]
    product_quantity: Optional[int]
    
class Service(ProductBase):
    product_status: str
    product_created_at: dt
    product_updated_at: dt

class productUpdate(BaseModel):
    product_name : Optional[str]
    product_price: Optional[int]
    product_quantity: Optional[int]