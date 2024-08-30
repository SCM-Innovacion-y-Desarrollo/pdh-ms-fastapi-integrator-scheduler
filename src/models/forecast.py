from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from ..models.declarative_base import Base

class Forecast(Base):
    __tablename__ = "forecast"

    forecast_id       = Column(Integer, primary_key=True)
    value             = Column(Integer, nullable=False)
    date              = Column(DateTime, nullable=False)
    path              = Column(String, nullable=False)