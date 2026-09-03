"""
Flight and Hotel Price Estimation Engine.
Estimates roundtrip airfare and lodging tiers based on Start (Origin) and End (Destination) locations.
"""
import numpy as np

def estimate_travel_logistics(dest_info: dict, travelers: int, nights: int, tier: str = "Boutique", origin: str = "New York, USA") -> dict:
    """
    Computes flight and accommodation expenses.
    origin: Start location string (e.g. 'New York, USA', 'London, UK', 'Mumbai, India')
    tier: 'Budget' | 'Boutique' | 'Luxury'
    """
    tier_key = tier if tier in ["Budget", "Boutique", "Luxury"] else "Boutique"
    dest_city = dest_info.get("city", "Destination")
    dest_country = dest_info.get("country", "")

    # Hash distance multiplier between origin and destination
    route_seed = abs(hash(f"{origin.lower()}->{dest_city.lower()}")) % 1000
    
    # Base airfare calculation based on route
    if origin.lower().split(",")[0] == dest_city.lower():
        # Domestic / Intra-city
        base_flight = 180.0
    elif any(region in origin.lower() for region in ["usa", "us", "america", "new york", "los angeles", "chicago"]) and any(region in dest_country.lower() for region in ["japan", "france", "italy", "uk", "spain", "thailand"]):
        base_flight = 850.0 + (route_seed % 350)
    else:
        base_flight = 650.0 + (route_seed % 450)

    multiplier = {"Budget": 0.75, "Boutique": 1.0, "Luxury": 1.9}
    per_person_flight = round(base_flight * multiplier[tier_key], 2)
    total_flights = per_person_flight * travelers

    # Hotel estimates
    rooms_needed = max(1, (travelers + 1) // 2)
    hotel_base = dest_info.get("hotel_estimate_usd_per_night", {})
    if isinstance(hotel_base, dict) and tier_key in hotel_base:
        per_night_hotel = hotel_base[tier_key]
    else:
        tier_rates = {"Budget": 75.0, "Boutique": 160.0, "Luxury": 420.0}
        per_night_hotel = tier_rates[tier_key]

    total_hotel = round(per_night_hotel * nights * rooms_needed, 2)

    # Daily food & transport
    food_base = dest_info.get("daily_food_usd", {})
    if isinstance(food_base, dict) and tier_key in food_base:
        per_day_food = food_base[tier_key]
    else:
        food_rates = {"Budget": 30.0, "Boutique": 70.0, "Luxury": 160.0}
        per_day_food = food_rates[tier_key]

    total_food = round(per_day_food * (nights + 1) * travelers, 2)

    return {
        "origin": origin,
        "destination": f"{dest_city}, {dest_country}".strip(", "),
        "flight_per_person": per_person_flight,
        "total_flights": round(total_flights, 2),
        "rooms_needed": rooms_needed,
        "hotel_per_night": per_night_hotel,
        "total_hotel": total_hotel,
        "food_per_person_day": per_day_food,
        "total_food": total_food,
        "logistics_total": round(total_flights + total_hotel + total_food, 2)
    }

