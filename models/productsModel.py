from email.policy import default
from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    product_pic = Column(String(255), nullable=False, unique=True)
    product_name = Column(String(255), nullable=False, unique=True)
    product_price = Column(Integer, nullable=False)
    product_discount = Column(Integer, nullable=True)
    product_quantity = Column(Integer, nullable=False)
    product_description = Column(String(255), nullable=False)
    product_status = Column(String(255), nullable=False, default="Active")
    product_created_at = Column(DateTime, default=text('NOW()'))
    product_updated_at = Column(DateTime, onupdate=text('NOW()'))

    order_product = relationship('Orders', back_populates='product_id', uselist = False)