# API Documentation

## Inference Service

### POST /predict
Predict whether an image is defective.

- Content-Type: `multipart/form-data`
- Body: `file` (image file)

Response:

```json
{
  "label": "defective",
  "confidence": 0.94,
  "details": "anomaly detected"
}
```

## Backend API

### POST /api/upload
Upload an image for defect detection and logging.

- Content-Type: `multipart/form-data`
- Body: `file` (image file)

Response:

```json
{
  "filename": "product-123.png",
  "label": "non-defective",
  "confidence": 0.87,
  "timestamp": "2026-05-03T12:34:56.789Z"
}
```

### GET /api/history
Fetch recent defect logs.

Response:

```json
{
  "events": [
    {
      "id": 1,
      "filename": "sample.png",
      "label": "defective",
      "confidence": 0.95,
      "created_at": "2026-05-03T12:34:56.789Z"
    }
  ]
}
```

### GET /api/stats
Fetch defect analytics and counts.

Response:

```json
{
  "total": 35,
  "defective": 12,
  "non_defective": 23,
  "recent": [ ... ]
}
```
