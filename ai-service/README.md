# AI Service

Inference service using Hugging Face Vision Transformer for defect detection.

## Files

- `api/main.py` - FastAPI application
- `inference/predict.py` - Model loading and prediction logic
- `training/train.py` - Fine-tuning script for custom datasets
- `Dockerfile` - Container image
- `requirements.txt` - Python dependencies

## Quick Start

### Local Development

```bash
pip install -r requirements.txt
python -c "from inference.predict import load_model; load_model()"
uvicorn api.main:app --reload --port 8001
```

### Docker

```bash
docker build -t ai-service .
docker run -p 8001:8001 ai-service
```

## Training

```bash
python training/train.py \
  --dataset_path /path/to/dataset \
  --output_dir ./model \
  --epochs 3 \
  --batch_size 16
```

## Model

- **Base:** google/vit-base-patch16-224
- **Fine-tuned:** Trained on defect detection data
- **Output:** {"label": "...", "confidence": ...}

## API

`POST /predict` - Classify an image

```bash
curl -X POST -F "file=@image.png" http://localhost:8001/predict
```

Response:

```json
{
  "label": "defective",
  "confidence": 0.94,
  "details": "anomaly detected"
}
```
