"""FastAPI Route Handlers"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from app.schemas.plan import (
    PlanRequest, PlanResponse, FlightLogistics, BudgetMatrix,
    DayItinerary, DaySchedule, HealthResponse, Airport, Hub
)
from app.services.flight_service import AIRPORTS, calculate_flight_logistics
from app.services.budget_service import calculate_budget_matrix
from app.services.itinerary_service import CURATED_HUBS, get_itinerary

router = APIRouter(prefix="/api", tags=["Travel Logistics"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for container orchestrators and monitoring."""
    return HealthResponse(
        status="healthy",
        service="aeroplan-prismatic-engine",
        version="1.0.0"
    )

@router.get("/airports", response_model=List[Airport])
async def list_airports():
    """List available departure airport hubs."""
    return [Airport(**a) for a in AIRPORTS.values()]

@router.get("/hubs", response_model=List[Hub])
async def list_curated_hubs():
    """List curated global destinations with coordinates and base rates."""
    return [Hub(**h) for h in CURATED_HUBS]

@router.post("/plan", response_model=PlanResponse)
async def generate_plan(payload: PlanRequest):
    """Generate complete route logistics, cost matrix, and day-by-day curated itinerary."""
    origin_key = payload.origin_id.upper().strip()
    if origin_key not in AIRPORTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Departure airport '{payload.origin_id}' not found. Available: {list(AIRPORTS.keys())}"
        )
    origin = AIRPORTS[origin_key]

    # Resolve destination coordinates
    dest_lat = payload.lat
    dest_lng = payload.lng
    dest_city = payload.dest_name
    dest_id = "custom"
    base_lodging = 240
    base_exp = 120

    # Match curated hub if applicable
    for hub in CURATED_HUBS:
        if (hub["name"].lower() in payload.dest_name.lower() or 
            payload.dest_name.lower() in hub["name"].lower() or 
            hub["city"].lower() in payload.dest_name.lower()):
            dest_id = hub["id"]
            dest_city = hub["city"]
            dest_lat = hub["lat"]
            dest_lng = hub["lng"]
            base_lodging = hub["lodging"]
            base_exp = hub["exp"]
            break

    if dest_lat is None or dest_lng is None:
        dest_lat = 35.6762
        dest_lng = 139.6503

    # Calculate flight logistics
    logistics = calculate_flight_logistics(
        origin["lat"], origin["lng"],
        dest_lat, dest_lng,
        payload.travel_class
    )

    # Calculate budget matrix
    budget = calculate_budget_matrix(
        flight_price=logistics["flight_price"],
        base_lodging=base_lodging,
        base_exp=base_exp,
        travel_class=payload.travel_class,
        days=payload.duration_days
    )

    # Generate distinct day-by-day itinerary
    itinerary_raw = get_itinerary(dest_id, dest_city, payload.duration_days)
    itinerary_days = [
        DayItinerary(
            day=d["day"],
            title=d["title"],
            theme=d["theme"],
            locations=d["locations"],
            schedule=DaySchedule(**d["schedule"]),
            culinary=d.get("culinary")
        )
        for d in itinerary_raw
    ]

    return PlanResponse(
        origin=origin,
        destination={
            "id": dest_id,
            "name": payload.dest_name,
            "city": dest_city,
            "lat": dest_lat,
            "lng": dest_lng
        },
        travel_class=payload.travel_class,
        duration_days=payload.duration_days,
        flight_logistics=FlightLogistics(
            origin_id=origin["id"],
            destination=dest_city,
            distance_km=logistics["distance_km"],
            flight_duration_str=logistics["flight_duration_str"],
            flight_price=logistics["flight_price"],
            non_stop=logistics["non_stop"]
        ),
        budget_matrix=budget,
        itinerary=itinerary_days
    )
