from src.models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time
from sqlalchemy.orm import relationship



class Shift(Base):
    __tablename__ = "shift"
    
    # Fields
    shift_id = Column(BigInteger, primary_key=True, autoincrement=True)
    employee_id = Column(BigInteger, nullable=False)
    date = Column(DateTime, nullable=False)
    start_ts = Column(DateTime, nullable=False)
    end_ts = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    timezone = Column(String, nullable=False)
    override = Column(Boolean, nullable=False)
    scheduler_create = Column(Boolean, nullable=False)
    enable = Column(Boolean, nullable=True)