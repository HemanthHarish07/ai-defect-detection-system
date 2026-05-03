from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import DefectLog


async def create_defect_log(session: AsyncSession, filename: str, label: str, confidence: float, details: str | None = None) -> DefectLog:
    log = DefectLog(filename=filename, label=label, confidence=confidence, details=details)
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log


async def get_history(session: AsyncSession, limit: int = 50):
    query = select(DefectLog).order_by(DefectLog.uploaded_at.desc()).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def get_stats(session: AsyncSession) -> dict:
    total_q = select(func.count(DefectLog.id))
    defective_q = select(func.count(DefectLog.id)).where(DefectLog.label == "defective")

    # 🔥 FIXED (underscore, not hyphen)
    non_defective_q = select(func.count(DefectLog.id)).where(DefectLog.label == "non_defective")

    total = (await session.execute(total_q)).scalar_one()
    defective = (await session.execute(defective_q)).scalar_one()
    non_defective = (await session.execute(non_defective_q)).scalar_one()

    return {
        "total": total,
        "defective": defective,
        "non_defective": non_defective,
    }