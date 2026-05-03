# Deployment Guide

## Prerequisites

- Docker and Docker Compose (>= 3.8)
- 4GB RAM minimum
- PostgreSQL 15+ (or use Docker PostgreSQL)

## Local Docker Deployment

### Step 1: Build the application

```bash
docker-compose build
```

### Step 2: Create .env file

```bash
cp .env.example .env
```

Update if necessary (defaults should work for local development):

```env
POSTGRES_URL=postgresql://postgres:07102004h@localhost:5432/defectdb
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
AI_SERVICE_URL=http://ai-service:8001
```

### Step 3: Start services

```bash
docker-compose up
```

Wait for all services to be running:

```
defect_db_1         | database system is ready to accept connections
ai-service_1        | Uvicorn running on 0.0.0.0:8001
backend_1           | Uvicorn running on 0.0.0.0:8000
frontend_1          | ready - started server on 0.0.0.0:3000
```

### Step 4: Access the dashboard

Open `http://localhost:3000` in your browser.

## Services Overview

| Service | Port | Endpoint | Purpose |
|---------|------|----------|---------|
| PostgreSQL | 5432 | `localhost:5432` | Database |
| AI Service | 8001 | `http://localhost:8001` | Model inference |
| Backend | 8000 | `http://localhost:8000/api` | API and logging |
| Frontend | 3000 | `http://localhost:3000` | Dashboard |

## Stopping Services

```bash
docker-compose down
```

Remove volumes:

```bash
docker-compose down -v
```

## Production Considerations

1. Use environment variables from secure vaults
2. Enable HTTPS/TLS in production
3. Use managed PostgreSQL service (RDS, Neon, etc.)
4. Add reverse proxy (nginx)
5. Set resource limits for containers
6. Use separate image registries for CI/CD
