"""Flight Mathematics and Airport Logistics Service"""
import math
from typing import Dict, Any

AIRPORTS: Dict[str, Dict[str, Any]] = {
    "JFK": {"id": "JFK", "name": "New York (JFK) — USA", "lat": 40.6413, "lng": -73.7781},
    "LHR": {"id": "LHR", "name": "London Heathrow (LHR) — UK", "lat": 51.4700, "lng": -0.4543},
    "HND": {"id": "HND", "name": "Tokyo Haneda (HND) — Japan", "lat": 35.5494, "lng": 139.7798},
    "DXB": {"id": "DXB", "name": "Dubai International (DXB) — UAE", "lat": 25.2532, "lng": 55.3657},
    "CDG": {"id": "CDG", "name": "Paris Charles de Gaulle (CDG) — France", "lat": 49.0097, "lng": 2.5479},
    "DEL": {"id": "DEL", "name": "Delhi Indira Gandhi (DEL) — India", "lat": 28.5562, "lng": 77.1000},
    "SIN": {"id": "SIN", "name": "Singapore Changi (SIN) — Singapore", "lat": 1.3644, "lng": 103.9915},
    "SYD": {"id": "SYD", "name": "Sydney Kingsford Smith (SYD) — Australia", "lat": -33.9399, "lng": 151.1753},
    "SFO": {"id": "SFO", "name": "San Francisco (SFO) — USA", "lat": 37.6213, "lng": -122.3790},
    "FRA": {"id": "FRA", "name": "Frankfurt Airport (FRA) — Germany", "lat": 50.0379, "lng": 8.5622}
}

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance in kilometers between two coordinates."""
    r = 6371.0  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c

def calculate_flight_logistics(origin_lat: float, origin_lng: float,
                               dest_lat: float, dest_lng: float,
                               travel_class: str = "curated") -> Dict[str, Any]:
    """Compute flight distance, flight duration string, and tier flight price."""
    dist = haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)
    
    class_mult = 1.75
    if travel_class.lower() == "economy":
        class_mult = 1.0
    elif travel_class.lower() == "first":
        class_mult = 3.4
        
    flight_price = round((150 + dist * 0.115) * class_mult)
    
    # Calculate flight duration (average cruising speed ~820 km/h)
    hours = max(1, int(dist // 820))
    mins = round((dist % 820) / (820 / 60))
    flight_duration_str = f"{hours}h {mins:02d}m"
    
    return {
        "distance_km": round(dist),
        "flight_duration_str": flight_duration_str,
        "flight_price": flight_price,
        "non_stop": True
    }
