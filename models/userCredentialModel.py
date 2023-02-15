from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User_credential(Base):
    __tablename__ = 'user_credential'

    user_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    user_email = Column(String(255), nullable=False)
    user_username = Column(String(255), nullable=False)
    user_password = Column(String(255), nullable=False)
    user_type = Column(Text, nullable=False)
    user_points = Column(String(255), nullable=True)
    user_status = Column(String(255), default="Active", nullable=False)
    # user_created_by = Column(String(255), nullable=False)
    # user_updated_by = Column(String(255), nullable=True)
    user_created_at = Column(DateTime, default=text('NOW()'))
    user_updated_at = Column(DateTime, onupdate=text('NOW()'))

    #admin
    # ad_user_credential = relationship('Admin', back_populates='user_credential', uselist = False)

    # #doctor
    dt_user_credential = relationship('Doctor', back_populates='user_credential', uselist = False)
    # dt_created_by = relationship('Doctor', back_populates='created_by')
    # dt_updated_by = relationship('Doctor', back_populates='updated_by')

    # #client
    cl_user_credential = relationship('Client', back_populates='user_credential', uselist = False)
    # cl_created_by = relationship('Client', foreign_keys = 'cl_created_by', back_populates='created_by')
    # cl_updated_by = relationship('Client', foreign_keys = 'cl_updated_by', back_populates='updated_by')

    # #employee
    em_user_credential = relationship('Employee', back_populates='user_credential', uselist = False)
    # em_created_by = relationship('Employee', back_populates='created_by')
    # em_updated_by = relationship('Employee', back_populates='updated_by')

    appointment_id = relationship('Appointment', back_populates='client_id', uselist = False)

    receipt_id = relationship('Receipt', back_populates='client_id', uselist = False)

    order_user = relationship('Orders', back_populates='user_id', uselist = False) 