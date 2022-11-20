from sqlalchemy import Integer, String, Text, DateTime, text, Time, Date
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Appointment(Base):
    __tablename__ = 'appointment'

    ap_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    ap_number = Column(String(255), nullable=True)
    ap_clientID = Column(String(36), ForeignKey('user_credential.user_id'),nullable=True)
    ap_date = Column(Date, nullable=True)
    ap_clientName = Column(String(255), nullable=True)
    ap_startTime = Column(Time, nullable=True)
    ap_endTime = Column(Time, nullable=True)
    ap_status = Column(String(255), nullable=True)
    ap_service = Column(String(255), nullable=True)
    ap_type = Column(String(255), nullable=True)
    ap_comorbidity = Column(String(255), nullable=True)
    ap_serviceType = Column(String(255), ForeignKey('service.service_id'), nullable=True)
    ap_amount = Column(Integer, nullable=True)
    ap_slotID = Column(String(255), ForeignKey('timeslot.slot_id'), nullable=True)
    ap_created_at = Column(DateTime, default=text('NOW()'))
    ap_updated_at = Column(DateTime, onupdate=text('NOW()'))

    client_id = relationship('User_credential', back_populates='appointment_id')

    service_id = relationship('Service', back_populates='service_app')

    
    slot_id = relationship('Timeslot', back_populates='slot_app')

    presc_id = relationship('Prescription', back_populates='appointment_id', uselist = False) 

    payment_id = relationship('Payment', back_populates='appointment_id', uselist = False)

    receipt_id = relationship('Receipt', back_populates='appointment_id', uselist = False)
    
