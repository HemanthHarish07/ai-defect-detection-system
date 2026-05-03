# Quick Reference

## Command Cheat Sheet

### Docker Commands

```bash
# Start all services
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f ai-service
docker-compose logs -f frontend

# Stop services
docker-compose down

# Full reset
docker-compose down -v

# Rebuild specific service
docker-compose build ai-service
```

### Frontend Commands

```bash
# Development
cd frontend
npm install
npm run dev

# Build
npm run build

# Testing
npm run cy:open
npm run cy:run
```

### Backend Commands

```bash
# Local dev (requires PostgreSQL running)
cd backend
pip install -r requirements.txt
export POSTGRES_URL=postgresql://postgres:07102004h@localhost:5432/defectdb
uvicorn main:app --reload
```

### AI Service Commands

```bash
# Local dev
cd ai-service
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8001

# Train model
python training/train.py --dataset_path ../sample_data/demo --output_dir ./model
```

### Database Commands

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d defectdb

# View defect logs
SELECT * FROM defect_logs ORDER BY uploaded_at DESC LIMIT 10;

# Count defects
SELECT label, COUNT(*) FROM defect_logs GROUP BY label;
```

---

## Service Endpoints

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Dashboard |
| Backend | http://localhost:8000/api | API |
| AI Service | http://localhost:8001 | Model inference |
| Database | localhost:5432 | PostgreSQL |

---

## API Endpoints

### POST /api/upload
Upload image and predict

```bash
curl -X POST -F "file=@image.png" http://localhost:8000/api/upload
```

### GET /api/history
Fetch recent logs

```bash
curl http://localhost:8000/api/history
```

### GET /api/stats
Fetch statistics

```bash
curl http://localhost:8000/api/stats
```

### POST /predict
Predict on image (AI service)

```bash
curl -X POST -F "file=@image.png" http://localhost:8001/predict
```

---

## File Locations

| Component | Root | Main File |
|-----------|------|-----------|
| Frontend | `frontend/` | `pages/index.js` |
| Backend | `backend/` | `main.py` |
| AI Service | `ai-service/` | `api/main.py` |
| Database | Docker compose | PostgreSQL:5432 |
| Docs | `docs/` | `SETUP.md` |

---

## Environment Variables

```env
POSTGRES_URL=postgresql://postgres:07102004h@localhost:5432/defectdb
AI_SERVICE_URL=http://ai-service:8001
NEXT_PUBLIC_BACKEND_URL=http://localhost:3000/api
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

---

## Ports

| Service | Port | Type |
|---------|------|------|
| Frontend | 3000 | HTTP |
| Backend | 8000 | HTTP |
| AI Service | 8001 | HTTP |
| PostgreSQL | 5432 | TCP |

---

## Testing Checklist

- [ ] Docker Compose starts all services
- [ ] Frontend loads at :3000
- [ ] Can upload image
- [ ] Prediction shows in dashboard
- [ ] History table updates
- [ ] Stats display correctly
- [ ] E2E tests pass

---

## Troubleshooting

**Service won't start?**
```bash
docker-compose logs <service>
```

**Port already in use?**
```bash
docker-compose down -v
```

**Model not loading?**
```bash
docker-compose exec ai-service ls -la model/
```

**Database connection failed?**
```bash
docker-compose exec db psql -U postgres -c "SELECT 1"
```

---

## Common Tasks

### Generate Sample Data
```bash
python sample_data/generate_samples.py --output sample_data/demo
```

### Train ViT Model
```bash
python ai-service/training/train.py --dataset_path sample_data/demo --output_dir ai-service/model
```

### Run E2E Tests
```bash
cd frontend && npm run cy:run
```

### View Database Contents
```bash
docker-compose exec db psql -U postgres -d defectdb -c "SELECT * FROM defect_logs;"
```

---

## Performance Tips

1. **Faster inference:** Enable GPU (nvidia-docker)
2. **Faster training:** Use larger batch size (16-32)
3. **Faster uploads:** Use smaller images (<5 MB)
4. **Faster frontend:** Clear browser cache

---

## Deployment Checklist

- [ ] .env configured with production values
- [ ] PostgreSQL running and accessible
- [ ] AI model trained and in `ai-service/model/`
- [ ] All services pass health checks
- [ ] E2E tests pass
- [ ] Docker images built
- [ ] Volumes mounted correctly
- [ ] Logs collection configured

---

**For detailed guides, see docs/ folder.**
