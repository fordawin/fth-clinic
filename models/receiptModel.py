from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.appointmentModel import Appointment

class Receipt(Base):
    __tablename__ = 'receipt'

    receipt_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    receipt_appointmentID = Column(String(255), ForeignKey('appointment.ap_id'), nullable=True)
    receipt_clientID = Column(String(255), ForeignKey('user_credential.user_id'), nullable=True)
    receipt_amount = Column(String(255), nullable=True)
    receipt_created_at = Column(DateTime, default=text('NOW()'))
    receipt_updated_at = Column(DateTime, onupdate=text('NOW()'))

    client_id = relationship('User_credential', back_populates='receipt_id')

    appointment_id = relationship('Appointment', back_populates='receipt_id')



    
