# Architecture Overview

## System Components

```
┌─────────────────┐          ┌──────────────────────┐
│    Frontend     │          │   AI Inference       │
│  (Next.js/MUI)  ├─────────→│  (FastAPI/ViT)       │
│  :3000          │          │  :8001               │
└────────┬────────┘          └──────────────────────┘
         │                             │
         │                             ↓
         │                   ┌──────────────────┐
         │                   │  Model & Weights │
         │                   │  (pytorch_model) │
         │                   └──────────────────┘
         ↓
    ┌──────────────────────┐
    │  Backend API         │
    │  (FastAPI)           │
    │  :8000               │
    └────────┬─────────────┘
             │
             ↓
    ┌──────────────────────┐
    │  PostgreSQL          │
    │  Defect Logs DB      │
    │  :5432               │
    └──────────────────────┘
```

## Data Flow: Image Upload

1. User uploads image via frontend
2. Frontend sends `POST /api/upload` to backend
3. Backend validates file (type, size)
4. Backend saves file locally to `uploads/`
5. Backend forwards image to `POST /predict` on AI service
6. AI service loads ViT model, runs inference
7. AI service returns `{"label": "...", "confidence": ...}`
8. Backend stores result in PostgreSQL
9. Backend returns result to frontend
10. Frontend displays result and refreshes dashboard

## Key Services

### Frontend (Next.js)

- **Role:** User interface for uploads and monitoring
- **Tech:** React 18, Material UI, Axios
- **Pages:**
  - `/` - Main dashboard with upload and history
- **Components:**
  - `UploadCard` - File upload interface
  - `StatsCard` - Summary statistics display
- **Services:**
  - `api.js` - HTTP client for backend communication

### Backend (FastAPI)

- **Role:** API gateway, file handling, database logging
- **Tech:** FastAPI, SQLAlchemy ORM, asyncpg
- **Endpoints:**
  - `POST /api/upload` - Upload and predict
  - `GET /api/history` - Fetch defect logs
  - `GET /api/stats` - Get statistics
- **Features:**
  - File validation (type, size)
  - Async database operations
  - Integration with AI service

### AI Service (FastAPI)

- **Role:** Model inference
- **Tech:** Transformers, PyTorch, FastAPI
- **Endpoints:**
  - `POST /predict` - Run model on image
- **Model:** Vision Transformer (google/vit-base-patch16-224)
- **Features:**
  - GPU support (auto-detects CUDA)
  - Loads fine-tuned model if available

### Database (PostgreSQL)

- **Role:** Persistent storage of defect logs
- **Table:** `defect_logs`
  - `id` (int) - Primary key
  - `filename` (str) - Original filename
  - `label` (str) - Prediction label
  - `confidence` (float) - Confidence score
  - `details` (str) - Additional info
  - `uploaded_at` (datetime) - Timestamp

## Deployment Architecture

### Docker Compose

Five containers orchestrated:

1. `db` - PostgreSQL database
2. `ai-service` - Model inference
3. `backend` - API and logging
4. `frontend` - Dashboard
5. Network bridge for inter-service communication

Volume mounts:

- `ai-service/model:/app/model` - Trained model
- `backend/uploads:/app/uploads` - Uploaded images
- `db_data:/var/lib/postgresql/data` - Database persistence

## Security Measures

1. **File Upload Validation**
   - Only PNG/JPEG accepted
   - Size limited to 5MB
   - Content-type checking

2. **Database**
   - Connection via environment variables
   - Prepared statements (SQLAlchemy ORM)

3. **API**
   - CORS not explicitly enabled (restrict if needed)
   - Error messages don't expose internals

## Performance Characteristics

| Operation | Typical Time |
|-----------|--------------|
| Model load | 2-5s (first time) |
| Single inference | 200-500ms (CPU) / 50-100ms (GPU) |
| API overhead | ~50ms |
| Database insert | ~10ms |
| **Total per upload** | **~300-600ms** |

## Scaling Considerations

For production:

1. Use load balancer in front of backend
2. Scale backend replicas independently
3. Use connection pooling for database
4. Cache model in memory per AI service
5. Use S3 or CDN for uploaded images
6. Add API rate limiting
