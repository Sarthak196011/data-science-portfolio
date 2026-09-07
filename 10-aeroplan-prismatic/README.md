# AEROPLAN PRISMATIC — Vivid 3D Route & Curated Itinerary Engine

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python)](https://python.org)
[![Three.js](https://img.shields.io/badge/Three.js-r128-black.svg?style=flat&logo=three.js)](https://threejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An interactive, chromatic 3D globe travel logistics and itinerary engine built with **FastAPI**, **Three.js**, **GSAP**, and **Pydantic**. 

Aeroplan Prismatic calculates real-time great-circle flight arcs, distances, tiered travel investments (Economy, Curated, First Class), and generates **rich, distinct day-by-day itineraries with exact locations, landmarks, schedules, and signature dining**.

---

## ✨ Features

- 🌍 **Vivid 3D Globe & Parabolic Flight Arcs**: Interactive Three.js sphere with illuminated airport pins, pulsating rings, chromatic atmosphere, and animated flight beacons.
- 🗓️ **Distinct Day-by-Day Itineraries**: 100% unique daily plans with exact locations covered each day (e.g. *Sensō-ji Temple*, *Shibuya Sky*, *teamLab Planets*).
- 🧭 **Timed Schedules**: Morning, afternoon, and evening breakdowns with landmark timings and curated dining recommendations.
- ⚡ **High-Performance FastAPI Backend**: RESTful architecture with Pydantic v2 data validation, CORS middleware, and automatic Swagger/OpenAPI interactive documentation.
- 📊 **Dynamic Cost Matrix**: Haversine distance calculations, flight duration estimates, and multi-tier budgets.
- 🧪 **Comprehensive Automated Testing**: Pytest suite covering all endpoints, validations, and itinerary uniqueness.
- 🐳 **Docker & Docker Compose**: Production-ready containerization for seamless cloud deployment.

---

## 🏗️ Architecture

```
aeroplan-prismatic/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py           # REST endpoints: /api/plan, /api/hubs, /api/airports, /api/health
│   │   ├── schemas/
│   │   │   └── plan.py             # Pydantic models for logistics, budgets, schedules
│   │   ├── services/
│   │   │   ├── flight_service.py   # Haversine distance, speed, flight time math
│   │   │   ├── itinerary_service.py# Curated 7-day hub database & procedural generator
│   │   │   └── budget_service.py   # Multi-tier cost calculation engine
│   │   ├── config.py               # Application settings
│   │   └── main.py                 # FastAPI app, CORS, static file mounts
│   └── tests/
│       └── test_api.py             # Pytest automated test suite
├── frontend/
│   ├── index.html                  # 3D interactive application interface
│   └── aeroplan_3d_vivid.html      # Standalone distribution
├── Dockerfile                      # Production Dockerfile
├── docker-compose.yml              # Docker Compose configuration
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Local Python Setup

```bash
# Clone the repository
git clone <repository_url>
cd aeroplan-prismatic

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI backend server
uvicorn backend.app.main:app --reload --port 8000
```

Once running, access:
- **Interactive Web App**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Redoc API**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 2. Docker & Docker Compose

Run the entire application in a container with one command:

```bash
docker compose up --build
```

Access the app at `http://localhost:8000`.

---

## 📡 API Reference

### `POST /api/plan`
Generates flight logistics, cost matrices, and distinct daily itineraries.

**Request Body:**
```json
{
  "origin_id": "JFK",
  "dest_name": "Tokyo, Japan",
  "travel_class": "curated",
  "duration_days": 3
}
```

**Response Example:**
```json
{
  "origin": {"id": "JFK", "name": "New York (JFK) — USA", "lat": 40.6413, "lng": -73.7781},
  "destination": {"id": "tokyo", "name": "Tokyo, Japan", "city": "Tokyo", "lat": 35.6762, "lng": 139.6503},
  "travel_class": "curated",
  "duration_days": 3,
  "flight_logistics": {
    "origin_id": "JFK",
    "destination": "Tokyo",
    "distance_km": 10853,
    "flight_duration_str": "13h 14m",
    "flight_price": 2447,
    "non_stop": true
  },
  "budget_matrix": {
    "formatted": {
      "flight_price": "$2,447",
      "lodging_nightly": "$372",
      "lodging_total": "$1,116",
      "daily_expenses": "$168",
      "total_expenses": "$504",
      "flight_and_stay": "$3,563",
      "total_budget": "$4,067"
    }
  },
  "itinerary": [
    {
      "day": 1,
      "title": "Ancient Heritage, Sumida Waters & Shibuya Skyline",
      "theme": "Historic Shrines & Neon Panoramas",
      "locations": ["Sensō-ji Temple", "Kaminarimon Gate", "Nakamise-dori", "Sumida River Cruise", "Shibuya Crossing", "Shibuya Sky"],
      "schedule": {
        "morning": "09:00 - 12:30: Historic Asakusa exploration...",
        "afternoon": "13:30 - 17:00: Board the futuristic Himiko water bus...",
        "evening": "18:30 - 21:30: Navigate lantern-lit alleys of Omoide Yokocho..."
      },
      "culinary": "Omoide Yokocho Yakitori & Shibuya Sky Horizon Cocktails"
    }
  ]
}
```

### `GET /api/airports`
Returns available departure airport hubs.

### `GET /api/hubs`
Returns curated global destinations with geographic coordinates and baseline costs.

### `GET /api/health`
Health check status for uptime monitoring.

---

## 🧪 Running Automated Tests

Run the full pytest suite:

```bash
pytest backend/tests -v
```

---

## 📄 License
MIT License. Open source and available for modification.
