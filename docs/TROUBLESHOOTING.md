# Troubleshooting Guide

## Common Issues

### 1. PostgreSQL Connection Fails

**Error:** `psycopg2.OperationalError: connection failed`

**Solutions:**

- Verify PostgreSQL is running: `docker-compose ps`
- Check connection string in `.env`
- Ensure port 5432 is available
- Wait for DB to be ready (30+ seconds after start)

### 2. AI Service Won't Start

**Error:** `RuntimeError: CUDA out of memory` or model loading fails

**Solutions:**

- Check disk space (model is ~340 MB)
- Reduce batch size in training if training locally
- Use CPU mode: model auto-detects no CUDA
- Monitor logs: `docker-compose logs ai-service`

### 3. Upload Fails

**Error:** `HTTP 500` when uploading

**Likely causes:**

- AI service unreachable from backend
- File type not PNG/JPEG
- File size > 5MB
- Database connection lost

**Debug:**

```bash
docker-compose logs backend
docker-compose logs ai-service
```

### 4. Frontend Won't Load

**Error:** Blank page or CORS error

**Solutions:**

- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_BACKEND_URL` environment variable
- Clear browser cache: Ctrl+Shift+Del

### 5. Model Inference is Slow

**Expected:** 200-500ms per image (CPU)

**Optimization:**

- Enable GPU support (requires nvidia-docker)
- Batch multiple images
- Use smaller ViT variant if available

### 6. Database Out of Space

**Solution:**

```bash
docker-compose down -v  # Remove old data
docker-compose up       # Fresh start
```

## Testing

### Manual API Testing

```bash
# Upload endpoint
curl -X POST -F "file=@sample.png" http://localhost:8000/api/upload

# History endpoint
curl http://localhost:8000/api/history

# Stats endpoint
curl http://localhost:8000/api/stats
```

### Model Testing

```bash
cd ai-service
python -c "from inference.predict import load_model, predict_image; from PIL import Image; m, p = load_model(); img = Image.open('test.png'); print(predict_image(img, m, p))"
```

### Cypress E2E Tests

```bash
cd frontend
npm run cy:run
```

## Performance Monitoring

### Check Docker Resource Usage

```bash
docker stats
```

### View Logs

```bash
docker-compose logs -f <service-name>
docker-compose logs backend
```

### Database Query Time

Connect to PostgreSQL:

```bash
docker-compose exec db psql -U postgres -d defectdb
```

Query logs:

```sql
SELECT COUNT(*) FROM defect_logs;
SELECT * FROM defect_logs ORDER BY uploaded_at DESC LIMIT 5;
```

## Reset Instructions

### Full Reset

```bash
docker-compose down -v
rm -rf backend/uploads/*
docker-compose up --build
```

### Database Only

```bash
docker-compose down
docker volume rm <project>_db_data
docker-compose up
```

### Model Reset

```bash
rm -rf ai-service/model
docker-compose build ai-service
docker-compose up
```

## Production Deployment

### Environment Variables

Use a `.env.production`:

```env
POSTGRES_URL=postgresql://user:pass@prod-db:5432/defectdb
AI_SERVICE_URL=https://ai.example.com
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

### Health Checks

Monitor endpoints:

- Backend: `GET http://backend:8000/`
- AI Service: `GET http://ai-service:8001/`

### Logging

Send logs to ELK stack or CloudWatch:

```bash
docker-compose logs --follow backend > /var/log/defect-backend.log
```

## Getting Help

1. Check service logs: `docker-compose logs <service>`
2. Verify network: `docker network ls`
3. Inspect database: `docker-compose exec db psql ...`
4. Review GitHub issues and tests
