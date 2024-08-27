from ..models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time, Date
from sqlalchemy.orm import relationship

class Availability(Base):
    
    __tablename__ = 'availability'

    availability_id = Column(BigInteger, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    data = Column(String(96), nullable=False)