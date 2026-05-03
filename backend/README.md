# Backend API

FastAPI backend for upload handling, logging, and defect analytics.

## Files

- `main.py` - Application entry point
- `config.py` - Configuration settings
- `db.py` - Database connection and setup
- `models.py` - SQLAlchemy models
- `schemas.py` - Pydantic request/response schemas
- `routes/upload.py` - Upload and prediction endpoint
- `routes/history.py` - History and stats endpoints
- `services/predict.py` - AI service integration
- `services/db_ops.py` - Database operations

## Quick Start

### Local Development

```bash
pip install -r requirements.txt
export POSTGRES_URL=postgresql://postgres:07102004h@localhost:5432/defectdb
export AI_SERVICE_URL=http://localhost:8001
uvicorn main:app --reload --port 8000
```

### Docker

```bash
docker build -t backend .
docker run -p 8000:8000 \
  -e POSTGRES_URL="postgresql://user:pass@db:5432/defectdb" \
  -e AI_SERVICE_URL="http://ai-service:8001" \
  backend
```

## API Endpoints

### POST /api/upload

Upload image and get prediction.

```bash
curl -X POST -F "file=@image.png" http://localhost:8000/api/upload
```

### GET /api/history

Fetch recent defect logs.

```bash
curl http://localhost:8000/api/history
```

### GET /api/stats

Fetch statistics.

```bash
curl http://localhost:8000/api/stats
```

## Database

- **Type:** PostgreSQL
- **Connection:** Via environment variable POSTGRES_URL
- **Auto-init:** Tables created on startup

## Environment Variables

- `POSTGRES_URL` - Database connection string
- `AI_SERVICE_URL` - URL to AI inference service
- `BACKEND_HOST` - Host (default: 0.0.0.0)
- `BACKEND_PORT` - Port (default: 8000)
- `UPLOAD_DIR` - Upload directory (default: uploads)
