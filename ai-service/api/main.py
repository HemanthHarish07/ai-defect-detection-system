import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from inference.predict import load_model, predict_image

app = FastAPI(
    title="Defect Detection AI Service",
    description="Inference service using Hugging Face Vision Transformer",
)

model, processor = load_model()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {exc}")

    result = predict_image(image, model, processor)
    return result

@app.get("/")
async def root():
    return {"status": "running", "service": "ai-service"}
