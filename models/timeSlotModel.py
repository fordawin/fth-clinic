from sqlalchemy import Integer, String, Text, DateTime, text, Date, Time
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Timeslot(Base):
    __tablename__ = 'timeslot'

    slot_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    slot_capacity = Column(String(255), nullable=True)
    slot_time = Column(Time, nullable=True)
    slot_date = Column(Date, nullable=True)
    slot_status = Column(String(255), nullable=True)

    slot_app = relationship('Appointment', back_populates='slot_id', uselist = False)   
    
