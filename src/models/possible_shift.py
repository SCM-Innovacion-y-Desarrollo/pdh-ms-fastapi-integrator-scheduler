from ..models.declarative_base import Base
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, Integer, Boolean, Time
from sqlalchemy.orm import relationship


class PossibleShift(Base):
    __tablename__ = "possible_shift"
    
    # Fields
    possible_shift_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)