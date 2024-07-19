from src.models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time
from sqlalchemy.orm import relationship

class RulesetAssignment(Base):
    __tablename__ = "ruleset_assignment"
    
    # Fields
    ruleset_assignment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    employee_id = Column(BigInteger, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    last_modified = Column(DateTime, nullable=True)

    # Foreign Keys
    ruleset_id = Column(BigInteger, ForeignKey("ruleset.ruleset_id"), nullable=False)
    
    # Relationships
    ruleset = relationship("Ruleset", back_populates="ruleset_assignments")