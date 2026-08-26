# ChurnShield MLOps Pipeline ⚙️

> **Production ML serving** | FastAPI + MLflow + Docker + GitHub Actions CI/CD

## Overview
Complete MLOps pipeline demonstrating the full production ML lifecycle: experiment tracking with MLflow, REST API serving with FastAPI, automated testing with pytest, containerization with Docker, and CI/CD with GitHub Actions.

## Quick Start
```bash
pip install -r requirements.txt
python src/train.py              # Train + MLflow tracking
uvicorn api.main:app --reload   # Start API server
pytest tests/ -v                # Run test suite
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | `/health`        | Health check + uptime |
| GET  | `/metrics`       | Request count + status |
| POST | `/predict`       | Single customer prediction |
| POST | `/predict/batch` | Batch predictions (up to 1000) |
| GET  | `/docs`          | Swagger UI (auto-generated) |

## Docker
```bash
docker build -t churnshield-api .
docker run -p 8000:8000 churnshield-api
# API → http://localhost:8000/docs
```

## CI/CD (GitHub Actions)
Push to `main` → Auto-runs:
1. Install dependencies
2. Train model
3. Run pytest suite
4. Build Docker image

## MLflow
```bash
mlflow ui --backend-store-uri ./mlruns
# Dashboard → http://localhost:5000
```
