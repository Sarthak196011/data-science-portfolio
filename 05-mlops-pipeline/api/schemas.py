"""Pydantic schemas for the MLOps API."""
from pydantic import BaseModel, Field
from typing import List, Optional

class PredictRequest(BaseModel):
    tenure_months:    int   = Field(..., ge=0, le=120, example=6)
    monthly_charges:  float = Field(..., ge=0, le=500, example=89.5)
    total_charges:    float = Field(..., ge=0,          example=537.0)
    num_products:     int   = Field(..., ge=1, le=10,   example=1)
    support_calls:    int   = Field(..., ge=0, le=20,   example=7)
    payment_delays:   int   = Field(..., ge=0, le=10,   example=3)
    contract_type:    str   = Field(..., example="Month-to-month")
    internet_service: str   = Field(..., example="Fiber optic")
    online_security:  str   = Field(..., example="No")
    tech_support:     str   = Field(..., example="No")
    paperless_billing:str   = Field(..., example="Yes")
    gender:           str   = Field(..., example="Female")
    senior_citizen:   int   = Field(..., ge=0, le=1, example=0)
    partner:          str   = Field(..., example="No")
    dependents:       str   = Field(..., example="No")

    class Config:
        json_schema_extra = {"example": {
            "tenure_months": 6, "monthly_charges": 89.5, "total_charges": 537.0,
            "num_products": 1, "support_calls": 7, "payment_delays": 3,
            "contract_type": "Month-to-month", "internet_service": "Fiber optic",
            "online_security": "No", "tech_support": "No", "paperless_billing": "Yes",
            "gender": "Female", "senior_citizen": 0, "partner": "No", "dependents": "No"
        }}

class PredictResponse(BaseModel):
    churn_probability: float
    churn_predicted:   bool
    risk_level:        str
    top_factors:       List[str]
    latency_ms:        float
    model_version:     str

class BatchRequest(BaseModel):
    customers: List[PredictRequest]

class BatchResponse(BaseModel):
    predictions: List[dict]
    total:        int
    latency_ms:   float

class HealthResponse(BaseModel):
    status:         str
    model_loaded:   bool
    uptime_seconds: float
    version:        str
