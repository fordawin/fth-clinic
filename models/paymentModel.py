from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    payment_mode = Column(String(255), nullable=True)
    payment_amount = Column(String(255), nullable=False)
    payment_appointmentID = Column(String(255), ForeignKey('appointment.ap_id'), nullable=True)
    payment_created_at = Column(DateTime, default=text('NOW()'))
    payment_updated_at = Column(DateTime, onupdate=text('NOW()'))

    appointment_id = relationship('Appointment', back_populates='payment_id')
