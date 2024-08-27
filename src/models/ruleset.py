from ..models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time, Float
from sqlalchemy.orm import relationship


class Ruleset(Base):
    __tablename__ = "ruleset"
    
    # Fields
    ruleset_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    min_daily_hours = Column(Float, nullable=False)
    max_daily_hours = Column(Float, nullable=False)
    min_weekly_hours = Column(Float, nullable=False)
    max_weekly_hours = Column(Float, nullable=False)
    min_hours_between_shifts = Column(Float, nullable=False)
    max_shift_segments_per_shift = Column(Integer, nullable=True)
    night_shift_start_time = Column(Time, nullable=True)
    night_shift_end_time = Column(Time, nullable=True)
    min_days_worked_per_week = Column(Integer, nullable=False)
    max_days_worked_per_week = Column(Integer, nullable=False)
    max_consecutive_work_days = Column(Integer, nullable=False)
    max_night_shifts_per_week = Column(Integer, nullable=False)
    max_consecutive_night_shifts = Column(Integer, nullable=True)
    min_days_between_night_shifts = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False)

    # Foreign Keys
    possible_shift_id = Column(Integer, ForeignKey("possible_shift.possible_shift_id"), nullable=False)

    
    # Relationships
    possible_shift = relationship("PossibleShift", back_populates="rulesets")
    ruleset_assignments = relationship("RulesetAssignment", back_populates="ruleset")
