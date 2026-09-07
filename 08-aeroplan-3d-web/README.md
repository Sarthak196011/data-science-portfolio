# AeroPlan Prismatic — Vivid 3D Engine & Travel Logistics Platform

An ultra-modern, interactive 3D flight trajectory and luxury travel planner featuring a Three.js WebGL globe, real-time airfare calculations, great-circle parabolic flight arcs, dynamic lodging estimators, and day-by-day curated itinerary generation.

## Features
- **Interactive Three.js 3D Earth**: Prismatic latitude/longitude rings, atmosphere glow shader, animated glowing origin and destination beacon markers, and live parabolic flight trajectories with traveling beacons.
- **Flight & Lodging Logistics Engine**: Real-time Haversine distance, airfare calculations across Economy, Curated Premium, and First Class, lodging multipliers, and comprehensive budget matrices.
- **Curated Trending Hubs**: Interactive selection across major world destinations (Tokyo, Reykjavik, Cairo, Paris, Bali, Rio de Janeiro, Cape Town, Zermatt, Santorini, Dubai).
- **Custom Plan Generator**: Slide-out glassmorphism drawer featuring detailed day-by-day itineraries (Morning / Afternoon / Evening activities), lodging recommendations, flight logistics, and JSON export.
- **FastAPI REST Backend**:
  - `GET /api/airports` — Global departure base hubs with coordinates.
  - `GET /api/destinations` — Curated trending destinations and highlights.
  - `GET /api/search?q=...` — Real-time destination search and coordinates.
  - `POST /api/plan` — High-performance travel matrix and itinerary computation.
  - `GET /api/health` — Service health check.

## Quick Start

### 1. Launch with Python / FastAPI
```bash
cd 08-aeroplan-3d-web
pip install -r requirements.txt
python server.py
```
Open **`http://localhost:8505`** in any web browser.

### 2. Standalone Offline Web App
Double-click `index.html` (or `aeroplan_3d_vivid.html`) to run directly in any web browser without any server dependencies.
