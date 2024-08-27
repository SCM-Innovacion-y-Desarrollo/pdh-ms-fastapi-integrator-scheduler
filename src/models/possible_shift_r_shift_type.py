from src.models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time
from sqlalchemy.orm import relationship


class PossibleShiftRShiftType(Base):
    __tablename__ = "possible_shift_r_shift_type"
    
    # Fields
    possible_shift_r_shift_type_id = Column(BigInteger, primary_key=True, autoincrement=True)
    monday = Column(Boolean, nullable=False)
    tuesday = Column(Boolean, nullable=False)
    wednesday = Column(Boolean, nullable=False)
    thursday = Column(Boolean, nullable=False)
    friday = Column(Boolean, nullable=False)
    saturday = Column(Boolean, nullable=False)
    sunday = Column(Boolean, nullable=False)
    break_period = Column(Integer, nullable=False)

    # Foreign Keys
    possible_shift_id = Column(Integer, ForeignKey("possible_shift.possible_shift_id"), nullable=False)
    shift_type_id = Column(Integer, ForeignKey("shift_type.shift_type_id"), nullable=False)

    
    # Relationships
    possible_shift = relationship("PossibleShift", back_populates="possible_shift_r_shift_types")
    shift_type = relationship("ShiftType", back_populates="possible_shift_r_shift_types")
