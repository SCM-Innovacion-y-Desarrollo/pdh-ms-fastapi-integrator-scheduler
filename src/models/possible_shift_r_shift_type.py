from src.models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time
from sqlalchemy.orm import relationship


class PossibleShiftRShiftType(Base):
    __tablename__ = "possible_shift_r_shift_type"
    
    # Fields
    possible_shift_r_shift_type_id = Column(BigInteger, primary_key=True, autoincrement=True)
    monday = Column(Boolean, nullable=True)
    tuesday = Column(Boolean, nullable=True)
    wednesday = Column(Boolean, nullable=True)
    thursday = Column(Boolean, nullable=True)
    friday = Column(Boolean, nullable=True)
    saturday = Column(Boolean, nullable=True)
    sunday = Column(Boolean, nullable=True)

    # Foreign Keys
    possible_shift_id = Column(BigInteger, ForeignKey("possible_shift.possible_shift_id"), nullable=False)
    shift_type_id = Column(BigInteger, ForeignKey("shift_type.shift_type_id"), nullable=False)

    
    # Relationships
    possible_shift = relationship("PossibleShift", back_populates="possible_shift_r_shift_types")
    shift_type = relationship("ShiftType", back_populates="possible_shift_r_shift_types")
