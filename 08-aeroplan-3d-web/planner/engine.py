"""
AeroPlan Prismatic Calculation Engine: Flight Logistics, Airfare, Lodging, and Itinerary Generator
"""
import math
from typing import Dict, Any, List
from .destinations import DEPARTURE_AIRPORTS, CURATED_DESTINATIONS

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on Earth in kilometers."""
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def get_airport_by_id(airport_id: str) -> Dict[str, Any]:
    for a in DEPARTURE_AIRPORTS:
        if a["id"].upper() == airport_id.upper() or a["code"].upper() == airport_id.upper():
            return a
    return DEPARTURE_AIRPORTS[0]

def find_destination(query_or_id: str) -> Dict[str, Any]:
    q = query_or_id.lower().strip()
    for d in CURATED_DESTINATIONS:
        if d["id"].lower() == q or q in d["name"].lower() or q in d["city"].lower() or q in d["country"].lower():
            return d
    # Fallback to Tokyo
    return CURATED_DESTINATIONS[0]

def compute_plan(origin_id: str, dest_id_or_name: str, travel_class: str = "curated", duration_days: int = 3, custom_lat: float = None, custom_lng: float = None) -> Dict[str, Any]:
    origin = get_airport_by_id(origin_id)
    
    # Destination resolution
    if custom_lat is not None and custom_lng is not None:
        dest = {
            "id": "custom",
            "name": dest_id_or_name or "Custom Earth Destination",
            "city": dest_id_or_name.split(",")[0] if "," in dest_id_or_name else dest_id_or_name,
            "country": dest_id_or_name.split(",")[1].strip() if "," in dest_id_or_name else "Global",
            "lat": custom_lat,
            "lng": custom_lng,
            "region": "International",
            "tags": ["Exploration", "Scenic", "Custom Route"],
            "base_daily_lodging": 250,
            "base_daily_expenses": 130,
            "hero_desc": f"Custom curated journey to {dest_id_or_name}.",
            "highlights": ["Iconic City Architecture", "Signature Culinary Experience", "Historic Downtown Discovery", "Sunset Horizon Vista"]
        }
    else:
        dest = find_destination(dest_id_or_name)

    dist_km = haversine_distance(origin["lat"], origin["lng"], dest["lat"], dest["lng"])
    dist_miles = dist_km * 0.621371

    # Flight duration (cruise speed ~820 km/h + 40 mins takeoff/approach)
    flight_hours = round((dist_km / 820.0) + 0.65, 1)
    flight_hours_str = f"{int(flight_hours)}h {int((flight_hours % 1) * 60)}m"

    # Class multipliers
    tier = travel_class.lower()
    if tier == "first class" or tier == "first":
        tier_label = "First Class"
        flight_mult = 3.4
        lodging_mult = 2.6
        expenses_mult = 2.2
        aircraft_type = "Boeing 777-300ER (Private First Suite)"
        hotel_tier_name = "Five-Star Luxury Palace / Signature Suite"
    elif tier == "curated":
        tier_label = "Curated Premium"
        flight_mult = 1.75
        lodging_mult = 1.55
        expenses_mult = 1.4
        aircraft_type = "Airbus A350-900 (Curated Premium Class)"
        hotel_tier_name = "Boutique Design Hotel / 5-Star Executive"
    else:
        tier_label = "Economy"
        flight_mult = 1.0
        lodging_mult = 1.0
        expenses_mult = 1.0
        aircraft_type = "Boeing 787-9 Dreamliner (Economy Comfort)"
        hotel_tier_name = "Premium 4-Star Central Hotel"

    # Flight Pricing: base boarding fare + rate per km
    base_airfare = 150 + (dist_km * 0.115)
    total_flight_price = round(base_airfare * flight_mult)

    # Lodging Pricing
    nightly_lodging = round(dest["base_daily_lodging"] * lodging_mult)
    total_lodging_price = nightly_lodging * duration_days

    # Daily food, transport & activities
    daily_expense = round(dest["base_daily_expenses"] * expenses_mult)
    total_activities_price = daily_expense * duration_days

    # Combined Matrix
    flight_and_stay = total_flight_price + total_lodging_price
    total_budget = flight_and_stay + total_activities_price
    carbon_kg = round(dist_km * 0.14)

    # Day-by-Day Detailed Itinerary Generation
    itinerary = []
    highlights = dest.get("highlights", ["Local Landmark", "Cultural Center", "Panoramic Viewpoint", "Culinary Tasting"])
    
    day_themes = [
        {"theme": "Arrival & Golden Hour Immersion", "focus": "Touchdown, luxury transfer, and sunset welcoming dinner"},
        {"theme": "Iconic Landmarks & Architectural Wonder", "focus": "Deep dive into world-renowned sights and historic masterpieces"},
        {"theme": "Hidden Enclaves & Artisanal Gastronomy", "focus": "Neighborhood culinary walks, secret gardens, and vibrant bazaars"},
        {"theme": "Nature Horizons & Coastal Excursion", "focus": "Outdoor panoramas, pristine waterways, and scenic retreats"},
        {"theme": "Art, Avant-Garde & High Culture", "focus": "Contemporary galleries, high-fashion avenues, and theatrical performances"},
        {"theme": "Peak Panorama & Twilight Celebration", "focus": "Helicopter or summit views followed by rooftop mixology"},
        {"theme": "Leisure Morning & Grand Departure", "focus": "Artisan souvenir curation, farewell brunch, and VIP private transfer"}
    ]

    for day_num in range(1, duration_days + 1):
        theme_info = day_themes[(day_num - 1) % len(day_themes)]
        highlight_idx = (day_num - 1) % len(highlights)
        main_highlight = highlights[highlight_idx]
        
        itinerary.append({
            "day": day_num,
            "title": f"Day {day_num} — {theme_info['theme']}",
            "description": theme_info['focus'],
            "schedule": {
                "morning": f"Morning private exploration of {main_highlight}. Exclusive VIP priority access before crowds.",
                "afternoon": f"Curated tasting lunch followed by an artisan walking tour through historic quarters.",
                "evening": f"Sunset panoramic cocktail session overlooking {dest['city']} skyline, followed by multi-course chef tasting dinner."
            }
        })

    # Recommended Accommodations
    hotels = [
        {
            "name": f"The Grand {dest['city']} Heritage Palace",
            "rating": 4.94,
            "nightly": nightly_lodging,
            "badge": "Signature Selection",
            "amenities": ["Panoramic City View", "Michelin-starred Dining", "Infinity Pool", "24/7 Butler Service"]
        },
        {
            "name": f"{dest['city']} Atelier Boutique & Spa",
            "rating": 4.88,
            "nightly": round(nightly_lodging * 0.88),
            "badge": "Design Excellence",
            "amenities": ["Organic Thermal Spa", "Artisan Coffee Bar", "Rooftop Garden", "Private Balcony"]
        }
    ]

    return {
        "origin": origin,
        "destination": dest,
        "travel_class": {
            "tier": tier,
            "label": tier_label,
            "aircraft": aircraft_type,
            "hotel_tier": hotel_tier_name
        },
        "duration_days": duration_days,
        "flight_logistics": {
            "distance_km": round(dist_km),
            "distance_miles": round(dist_miles),
            "flight_hours": flight_hours,
            "flight_duration_str": flight_hours_str,
            "carbon_kg": carbon_kg,
            "route_status": "Non-Stop Direct Flight Available"
        },
        "budget_matrix": {
            "flight_price": total_flight_price,
            "nightly_lodging": nightly_lodging,
            "lodging_total": total_lodging_price,
            "flight_and_stay": flight_and_stay,
            "daily_expenses": daily_expense,
            "activities_total": total_activities_price,
            "total_budget": total_budget,
            "currency": "USD",
            "formatted": {
                "flight_and_stay": f"${flight_and_stay:,}",
                "total_budget": f"${total_budget:,}",
                "flight_price": f"${total_flight_price:,}",
                "lodging_total": f"${total_lodging_price:,}"
            }
        },
        "itinerary": itinerary,
        "recommended_hotels": hotels
    }
