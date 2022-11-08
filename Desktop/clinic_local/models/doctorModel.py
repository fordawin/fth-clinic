from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Doctor(Base):
    __tablename__ = 'doctor'

    dt_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    dt_pic = Column(Text, nullable=True)
    dt_firstName = Column(String(255), nullable=False)
    dt_middleName = Column(String(255), nullable=True)
    dt_lastName = Column(String(255), nullable=False)
    dt_fullName = Column(String(255), nullable=False)
    dt_houseNo = Column(String(255), nullable=False)
    dt_street = Column(String(255), nullable=False)
    dt_brgy = Column(String(255), nullable=False)
    dt_city = Column(String(255), nullable=False)
    dt_address = Column(String(255), nullable=False)
    dt_status = Column(String(255), nullable=False)
    dt_contactNo = Column(String(255), nullable=False)
    dt_user_credential = Column(String(255), ForeignKey('user_credential.user_id'), nullable=False)
    # dt_created_by = Column(String(255), ForeignKey('user_credential.user_id'), nullable=True)
    # dt_updated_by = Column(String(255), ForeignKey('user_credential.user_id'), nullable=True)
    dt_created_at = Column(DateTime, default=text('NOW()'))
    dt_updated_at = Column(DateTime, onupdate=text('NOW()'))

    #doctor
    user_credential = relationship('User_credential', back_populates='dt_user_credential')
    # created_by = relationship('User_credential', foreign_keys='Doctor.dt_created_by', back_populates='doctor')
    # updated_by = relationship('User_credential', foreign_keys='Doctor.dt_updated_by', back_populates='doctor')
