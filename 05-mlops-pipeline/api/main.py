"""
MLOps Pipeline — FastAPI serving app
Endpoints: POST /predict, GET /health, GET /metrics, GET /docs
Run: uvicorn api.main:app --reload
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import PredictRequest, PredictResponse, BatchRequest, BatchResponse, HealthResponse
from src.predict import load_model, predict_single, predict_batch
import time, os

app = FastAPI(
    title="ChurnShield MLOps API",
    description="Production ML serving endpoint for customer churn prediction. Built with FastAPI + MLflow.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Startup ────────────────────────────────────────────────────────────────────
_model_artifacts = None
_request_count   = 0
_start_time      = time.time()

@app.on_event("startup")
async def startup():
    global _model_artifacts
    _model_artifacts = load_model()
    print(f"[MLOps] Model loaded: {type(_model_artifacts['model']).__name__}")

# ── Health ─────────────────────────────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
def health():
    return HealthResponse(
        status="healthy",
        model_loaded=_model_artifacts is not None,
        uptime_seconds=round(time.time() - _start_time, 1),
        version="1.0.0",
    )

# ── Metrics ────────────────────────────────────────────────────────────────────
@app.get("/metrics", tags=["Monitoring"])
def metrics():
    return {
        "requests_total": _request_count,
        "uptime_seconds": round(time.time() - _start_time, 1),
        "model_version": "v1.0",
        "status": "ok",
    }

# ── Single Prediction ──────────────────────────────────────────────────────────
@app.post("/predict", response_model=PredictResponse, tags=["Inference"])
def predict(req: PredictRequest):
    global _request_count
    _request_count += 1

    if _model_artifacts is None:
        raise HTTPException(503, "Model not loaded. Run training first.")

    start = time.time()
    result = predict_single(_model_artifacts, req.dict())
    latency = round((time.time() - start) * 1000, 2)

    return PredictResponse(
        churn_probability=result["probability"],
        churn_predicted=result["predicted"],
        risk_level=result["risk_level"],
        top_factors=result["top_factors"],
        latency_ms=latency,
        model_version="v1.0",
    )

# ── Batch Prediction ───────────────────────────────────────────────────────────
@app.post("/predict/batch", response_model=BatchResponse, tags=["Inference"])
def predict_batch_endpoint(req: BatchRequest):
    global _request_count
    _request_count += len(req.customers)

    if _model_artifacts is None:
        raise HTTPException(503, "Model not loaded.")
    if len(req.customers) > 1000:
        raise HTTPException(400, "Batch size cannot exceed 1000.")

    start = time.time()
    results = predict_batch(_model_artifacts, [c.dict() for c in req.customers])
    latency = round((time.time() - start) * 1000, 2)

    return BatchResponse(predictions=results, total=len(results), latency_ms=latency)
