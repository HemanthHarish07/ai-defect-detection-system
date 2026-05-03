import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from db import create_db_tables
from routes.upload import router as upload_router
from routes.history import router as history_router


app = FastAPI(
    title="Defect Detection Backend",
    description="API layer for uploads, logging, and analytics",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Dev only — later restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(upload_router)
app.include_router(history_router)


@app.on_event("startup")
async def startup_event():
    await create_db_tables()



@app.get("/")
async def root():
    return {"status": "healthy", "service": "backend"}



if __name__ == "__main__":
    uvicorn.run(
        "main:app",   # 🔥 important: use string reference
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True   # optional for dev
    )