import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from db import AsyncSessionLocal
from services.predict import invoke_ai_service
from services.db_ops import create_defect_log
from schemas import DefectResult

router = APIRouter(prefix="/api", tags=["upload"])

VALID_TYPES = {"image/png", "image/jpeg", "image/jpg"}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/upload", response_model=DefectResult)
async def upload_image(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    if file.content_type not in VALID_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG and PNG images are supported.")

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Limit is 5MB.")

    filename = os.path.basename(file.filename)
    save_path = os.path.join(settings.UPLOAD_DIR, filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    with open(save_path, "wb") as f:
        f.write(contents)

    
    prediction = await invoke_ai_service(filename, contents, file.content_type)

    raw_label = prediction.get("label")
    confidence = float(prediction.get("confidence", 0.0))

    
    if confidence >= 0.5:
        clean_label = "non_defective"
    else:
        clean_label = "defective"

    details = f"Predicted as {clean_label} with confidence {confidence:.2f}"

    
    log = await create_defect_log(session, filename, clean_label, confidence, details)

    return {
        "filename": log.filename,
        "label": log.label,
        "confidence": log.confidence,
        "details": log.details,
        "timestamp": log.uploaded_at,
    }