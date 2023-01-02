from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Client(Base):
    __tablename__ = 'client'

    cl_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    cl_pic = Column(String(255), nullable=True)
    cl_firstName = Column(String(255), nullable=False)
    cl_middleName = Column(String(255), nullable=True)
    cl_lastName = Column(String(255), nullable=False)
    cl_fullName = Column(String(255), nullable=True)
    cl_houseNo = Column(String(255), nullable=False)
    cl_street = Column(String(255), nullable=False)
    cl_brgy = Column(String(255), nullable=False)
    cl_city = Column(String(255), nullable=False)
    cl_address = Column(String(255), nullable=True)
    cl_status = Column(String(255), nullable=False)
    cl_maritalStatus = Column(String(255), nullable=True)
    cl_birthdate = Column(String(255), nullable=False)
    cl_gender = Column(String(255), nullable=False)
    cl_contactNo = Column(String(255), nullable=False)
    cl_user_credential = Column(String(255), ForeignKey('user_credential.user_id'), nullable=False)
    # cl_created_by = Column(String(255), ForeignKey('user_credential.user_id'), nullable=True)
    # cl_updated_by = Column(String(255), ForeignKey('user_credential.user_id'), nullable=True)
    cl_created_at = Column(DateTime, default=text('NOW()'))
    cl_updated_at = Column(DateTime, onupdate=text('NOW()'))

    #user credentials
    user_credential = relationship('User_credential', back_populates='cl_user_credential')
    # created_by = relationship('User_credential', foreign_keys = 'cl_created_by', back_populates='cl_created_by')
    # updated_by = relationship('User_credential', foreign_keys = 'cl_updated_by', back_populates='cl_updated_by')

    # receipt_id = relationship('Receipt', back_populates='client_id', uselist = False)
