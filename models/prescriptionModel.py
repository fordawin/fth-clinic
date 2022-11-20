from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Prescription(Base):
    __tablename__ = 'prescription'

    presc_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    presc_appointmentID = Column(String(255), ForeignKey('appointment.ap_id'), nullable=True)
    presc_medication = Column(String(255), nullable=False)
    presc_treatment = Column(String(255), nullable=True)
    presc_remarks = Column(String(255), nullable=True)
    presc_created_at = Column(DateTime, default=text('NOW()'))
    presc_updated_at = Column(DateTime, onupdate=text('NOW()'))

    appointment_id = relationship('Appointment', back_populates='presc_id')  
    
    