"""pytest test suite for the MLOps API."""
import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))
from api.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

SAMPLE = {
    "tenure_months":6,"monthly_charges":89.5,"total_charges":537.0,
    "num_products":1,"support_calls":7,"payment_delays":3,
    "contract_type":"Month-to-month","internet_service":"Fiber optic",
    "online_security":"No","tech_support":"No","paperless_billing":"Yes",
    "gender":"Female","senior_citizen":0,"partner":"No","dependents":"No"
}

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data

def test_predict_returns_200(client):
    r = client.post("/predict", json=SAMPLE)
    assert r.status_code == 200

def test_predict_response_schema(client):
    r = client.post("/predict", json=SAMPLE)
    data = r.json()
    assert "churn_probability" in data
    assert "churn_predicted"   in data
    assert "risk_level"        in data
    assert "top_factors"       in data
    assert 0 <= data["churn_probability"] <= 1

def test_predict_probability_range(client):
    r = client.post("/predict", json=SAMPLE)
    p = r.json()["churn_probability"]
    assert 0.0 <= p <= 1.0

def test_predict_risk_level_valid(client):
    r = client.post("/predict", json=SAMPLE)
    assert r.json()["risk_level"] in ["High","Medium","Low"]

def test_batch_predict(client):
    r = client.post("/predict/batch", json={"customers":[SAMPLE, SAMPLE]})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["predictions"]) == 2

def test_metrics_endpoint(client):
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "requests_total" in r.json()

def test_invalid_payload(client):
    r = client.post("/predict", json={"bad_field": 999})
    assert r.status_code == 422
