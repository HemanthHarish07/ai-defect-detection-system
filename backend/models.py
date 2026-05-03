from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String
from db import Base

class DefectLog(Base):
    __tablename__ = "defect_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(256), nullable=False)
    label = Column(String(64), nullable=False)
    confidence = Column(Float, nullable=False)
    details = Column(String(512), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
