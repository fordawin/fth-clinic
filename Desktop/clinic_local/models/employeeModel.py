from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = 'employee'

    em_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    em_pic = Column(String(255), nullable=True)
    em_firstName = Column(String(255), nullable=False)
    em_middleName = Column(String(255), nullable=True)
    em_lastName = Column(String(255), nullable=False)
    em_fullName = Column(String(255), nullable=False)
    em_houseNo = Column(String(255), nullable=False)
    em_street = Column(String(255), nullable=False)
    em_brgy = Column(String(255), nullable=False)
    em_city = Column(String(255), nullable=False)
    em_address = Column(String(255), nullable=False)
    em_status = Column(String(255), nullable=False)
    em_contactNo = Column(String(255), nullable=False)
    em_user_credential = Column(String(255), ForeignKey('user_credential.user_id'), nullable=False)
    # em_created_by = Column(String(255), ForeignKey('user_credential.user_id'), nullable=False)
    # em_updated_by = Column(String(255), ForeignKey('user_credential.user_id'), nullable=True)
    em_created_at = Column(DateTime, default=text('NOW()'))
    em_updated_at = Column(DateTime, onupdate=text('NOW()'))

    #user credentials
    user_credential = relationship('User_credential', back_populates='em_user_credential')
    # created_by = relationship('User_credential', back_populates='employee')
    # updated_by = relationship('User_credential', back_populates='employee')

