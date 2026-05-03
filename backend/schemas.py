from datetime import datetime
from pydantic import BaseModel

class DefectResult(BaseModel):
    filename: str
    label: str
    confidence: float
    details: str | None = None
    timestamp: datetime

    class Config:
        orm_mode = True

class HistoryItem(BaseModel):
    id: int
    filename: str
    label: str
    confidence: float
    uploaded_at: datetime

    class Config:
        orm_mode = True

class StatsResponse(BaseModel):
    total: int
    defective: int
    non_defective: int
