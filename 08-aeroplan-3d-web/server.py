"""
AeroPlan Prismatic — High-Performance FastAPI Backend Server
Serves 3D Flight Planner Web Application and Travel Intelligence REST APIs
"""
import os
import sys
from typing import Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Ensure planner module is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from planner.destinations import DEPARTURE_AIRPORTS, CURATED_DESTINATIONS
from planner.engine import compute_plan, find_destination, haversine_distance

app = FastAPI(
    title="AeroPlan Prismatic API",
    description="Vivid 3D Flight Navigation & Intelligent Travel Itinerary Platform",
    version="2.0.0"
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic request models
class PlanRequest(BaseModel):
    origin_id: str = "JFK"
    dest_name: str = "Tokyo, Japan"
    travel_class: str = "curated"
    duration_days: int = 3
    lat: Optional[float] = None
    lng: Optional[float] = None

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AeroPlan Prismatic Vivid 3D Engine",
        "version": "2.0.0"
    }

@app.get("/api/airports")
def get_airports():
    """Retrieve all available departure base hubs with coordinates."""
    return {"airports": DEPARTURE_AIRPORTS}

@app.get("/api/destinations")
def get_destinations():
    """Retrieve curated trending hubs."""
    return {"destinations": CURATED_DESTINATIONS}

@app.get("/api/search")
def search_destinations(q: str = Query(..., min_length=1)):
    """Search for destinations by name, region, tags, or country."""
    query = q.lower().strip()
    results = []
    for d in CURATED_DESTINATIONS:
        if (query in d["name"].lower() or 
            query in d["city"].lower() or 
            query in d["country"].lower() or 
            query in d["region"].lower() or 
            any(query in t.lower() for t in d.get("tags", []))):
            results.append(d)
    
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

@app.post("/api/plan")
def create_travel_plan(req: PlanRequest):
    """Generate complete flight logistics, lodging tiers, budget matrix, and day-by-day itinerary."""
    plan = compute_plan(
        origin_id=req.origin_id,
        dest_id_or_name=req.dest_name,
        travel_class=req.travel_class,
        duration_days=req.duration_days,
        custom_lat=req.lat,
        custom_lng=req.lng
    )
    return plan

# Static files directory
static_dir = os.path.join(current_dir, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    """Serve the interactive AeroPlan Prismatic web application."""
    index_path = os.path.join(static_dir, "index.html") if os.path.exists(os.path.join(static_dir, "index.html")) else os.path.join(current_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "AeroPlan Prismatic API is online. Frontend static files pending."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8505))
    print(f"[AeroPlan] Starting AeroPlan Prismatic Server on http://localhost:{port}")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
