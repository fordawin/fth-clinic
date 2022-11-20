from email.policy import default
from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship
from database import Base

class Service(Base):
    __tablename__ = 'service'

    service_id = Column(String(36), primary_key=True, default=text('gen_random_uuid()'))
    service_name = Column(String(255), nullable=False, unique=True)
    service_price = Column(Integer, nullable=False)
    service_description = Column(String(255), nullable=False)
    service_status = Column(String(255), nullable=False, default="Active")
    service_created_at = Column(DateTime, default=text('NOW()'))
    service_updated_at = Column(DateTime, onupdate=text('NOW()'))

    service_app = relationship('Appointment', back_populates='service_id', uselist = False)
