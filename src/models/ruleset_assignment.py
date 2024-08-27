from ..models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time, Date
from sqlalchemy.orm import relationship

class RulesetAssignment(Base):
    __tablename__ = "ruleset_assignment"
    
    # Fields
    ruleset_assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    last_modified = Column(Date, nullable=True)

    # Foreign Keys
    ruleset_id = Column(Integer, ForeignKey("ruleset.ruleset_id"), nullable=False)
    
    # Relationships
    ruleset = relationship("Ruleset", back_populates="ruleset_assignments")