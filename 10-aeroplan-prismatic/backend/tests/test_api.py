"""Automated Test Suite for Aeroplan Prismatic API"""
import pytest
import sys
import os

# Add backend directory to path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "aeroplan-prismatic-engine"

def test_list_airports():
    response = client.get("/api/airports")
    assert response.status_code == 200
    airports = response.json()
    assert len(airports) >= 10
    ids = [a["id"] for a in airports]
    assert "JFK" in ids
    assert "HND" in ids

def test_list_hubs():
    response = client.get("/api/hubs")
    assert response.status_code == 200
    hubs = response.json()
    assert len(hubs) >= 10
    cities = [h["city"] for h in hubs]
    assert "Tokyo" in cities
    assert "Paris" in cities
    assert "Reykjavik" in cities

def test_plan_generation_tokyo():
    payload = {
        "origin_id": "JFK",
        "dest_name": "Tokyo, Japan",
        "travel_class": "curated",
        "duration_days": 3
    }
    response = client.post("/api/plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["travel_class"] == "curated"
    assert data["duration_days"] == 3
    assert data["flight_logistics"]["distance_km"] > 10000
    assert "itinerary" in data
    assert len(data["itinerary"]) == 3

    # Verify that every day is distinct and has exact locations
    itinerary = data["itinerary"]
    titles = [d["title"] for d in itinerary]
    assert len(set(titles)) == 3, "Day titles must be completely unique"

    for d in itinerary:
        assert len(d["locations"]) >= 3, "Each day must have exact locations"
        assert d["schedule"]["morning"] != ""
        assert d["schedule"]["afternoon"] != ""
        assert d["schedule"]["evening"] != ""

def test_plan_distinct_7_days():
    payload = {
        "origin_id": "LHR",
        "dest_name": "Paris, France",
        "travel_class": "first",
        "duration_days": 7
    }
    response = client.post("/api/plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    itinerary = data["itinerary"]
    assert len(itinerary) == 7
    titles = [d["title"] for d in itinerary]
    assert len(set(titles)) == 7, "All 7 days must be completely distinct"

def test_custom_destination_generation():
    payload = {
        "origin_id": "JFK",
        "dest_name": "Rome, Italy",
        "travel_class": "economy",
        "duration_days": 4,
        "lat": 41.9028,
        "lng": 12.4964
    }
    response = client.post("/api/plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    itinerary = data["itinerary"]
    assert len(itinerary) == 4
    for d in itinerary:
        assert "Rome" in d["locations"][0]

def test_invalid_origin_airport():
    payload = {
        "origin_id": "INVALID",
        "dest_name": "Tokyo, Japan",
        "travel_class": "curated",
        "duration_days": 3
    }
    response = client.post("/api/plan", json=payload)
    assert response.status_code == 404
