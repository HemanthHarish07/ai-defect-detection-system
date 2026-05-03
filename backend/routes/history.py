from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import AsyncSessionLocal
from services.db_ops import get_history, get_stats
from schemas import HistoryItem, StatsResponse

router = APIRouter(prefix="/api", tags=["history"])

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/history", response_model=list[HistoryItem])
async def history(session: AsyncSession = Depends(get_session)):
    return await get_history(session)

@router.get("/stats", response_model=StatsResponse)
async def stats(session: AsyncSession = Depends(get_session)):
    return await get_stats(session)
