from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Admin(Base):
    __tablename__ = 'admin'

    ad_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    ad_user_credential = Column(String(255), ForeignKey('user_credential.user_id'), nullable=False)

    #user credentials
    # user_credential = relationship('User_credential', back_populates='admin')

