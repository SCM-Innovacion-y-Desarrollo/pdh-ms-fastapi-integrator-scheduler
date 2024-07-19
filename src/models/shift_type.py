from src.models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time
from sqlalchemy.orm import relationship


class ShiftType(Base):
    __tablename__ = "shift_type"
    
    # Fields
    shift_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration = Column(Time, nullable=False)
    
    # Relationships
    possible_shift_r_shift_types = relationship("PossibleShiftRShiftType", back_populates="shift_type")
