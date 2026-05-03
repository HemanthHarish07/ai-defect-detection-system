# Setup Guide

## 1. Install prerequisites

- Docker and Docker Compose
- Python 3.11
- Node.js 20+
- PostgreSQL if running without Docker

## 2. Prepare the MVTec AD dataset

1. Download the MVTec AD dataset from the official website.
2. Extract the archive.
3. Create a folder structure for training:

```text
/path/to/dataset/
  normal/
    image1.png
    image2.png
  defective/
    defect1.png
    defect2.png
```

4. Use the sample generator if you need example images:

```bash
python sample_data/generate_samples.py --output sample_data/demo
```

## 3. Train the model

From `ai-service/`:

```bash
cd ai-service
python training/train.py --dataset_path ../sample_data/demo --output_dir ./model --epochs 2 --batch_size 8
```

This creates a local ViT model in `ai-service/model`.

## 4. Configure environment

Copy `.env.example` to `.env` and adjust values if necessary:

```bash
cp .env.example .env
```

## 5. Start services with Docker

```bash
docker-compose up --build
```

The system will be available at `http://localhost:3000`.

## 6. Verify services

- AI service: `http://localhost:8001`
- Backend API: `http://localhost:8000/api`
- Frontend: `http://localhost:3000`

## 7. Running tests

From the repository root:

```bash
cd frontend
npm run cy:run
```

## 8. Notes

- If using a local PostgreSQL instance, ensure `POSTGRES_URL` in `.env` points to your database.
- The backend creates tables automatically at startup.
