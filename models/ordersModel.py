from email.policy import default
from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    order_quantity = Column(Integer, nullable=False)
    order_total = Column(Integer, nullable=False)
    order_productid = Column(String(255), ForeignKey('product.product_id'), nullable=True)
    order_userid = Column(String(255), ForeignKey('user_credential.user_id'), nullable=True)
    order_remarks = Column(String(255), nullable=False)
    order_user = Column(String(255), nullable=False)
    order_status = Column(String(255), nullable=False, default="Pending")
    order_created_at = Column(DateTime, default=text('NOW()'))
    order_updated_at = Column(DateTime, onupdate=text('NOW()'))

    user_id = relationship('User_credential', back_populates='order_user')

    product_id = relationship('Product', back_populates='order_product')