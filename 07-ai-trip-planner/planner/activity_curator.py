"""
Activity Curation & Global Location Resolution Engine.
Filters and scores places based on user interest tags and travel intensity.
Synthesizes dynamic itineraries for ANY start and end location in the world.
"""
import numpy as np
import re

def resolve_global_destination(location_query: str, catalog_destinations: list) -> dict:
    """
    Resolves a location query against catalog or dynamically synthesizes
    a rich destination profile for ANY location in the world.
    """
    clean_q = location_query.strip().lower()
    
    # 1. Match catalog
    for d in catalog_destinations:
        matched_str = f"{d['city']}, {d['country']}".lower()
        if clean_q in d["city"].lower() or d["city"].lower() in clean_q or clean_q in matched_str:
            return d

    # 2. Synthesize dynamic profile for ANY custom world destination
    parts = [p.strip().title() for p in location_query.split(",") if p.strip()]
    city_name = parts[0] if parts else location_query.title()
    country_name = parts[1] if len(parts) > 1 else "Global Destination"

    seed = abs(hash(location_query.lower())) % (2**32)
    np.random.seed(seed)

    taglines = [
        f"A breathtaking destination renowned for rich cultural heritage and vibrant local experiences.",
        f"Discover picturesque streets, world-class gastronomy, and unforgettable historic landmarks in {city_name}.",
        f"Experience stunning scenery, iconic city vistas, and unique local traditions."
    ]

    custom_activities = [
        {"name": f"{city_name} Historic City Center Walking Tour", "category": "Culture", "neighborhood": "Old Town", "cost_usd": 0.0, "duration_hours": 2.5, "rating": 4.8, "desc": f"Guided stroll through iconic architectural squares and historic monuments in {city_name}."},
        {"name": f"Authentic {city_name} Culinary & Street Food Tasting", "category": "Food", "neighborhood": "Central Market", "cost_usd": 32.0, "duration_hours": 2.0, "rating": 4.9, "desc": f"Sample regional delicacies, traditional spices, and popular local dishes."},
        {"name": f"{city_name} Panoramic Skyline Observation & Sunset Point", "category": "Sightseeing", "neighborhood": "Downtown", "cost_usd": 18.0, "duration_hours": 1.5, "rating": 4.7, "desc": f"Breathtaking 360-degree viewpoint over the entire city and surrounding landscape."},
        {"name": f"National Museum & Heritage Art Gallery", "category": "Culture", "neighborhood": "Museum Quarter", "cost_usd": 15.0, "duration_hours": 3.0, "rating": 4.8, "desc": f"Discover priceless historical artifacts and masterwork art collections."},
        {"name": f"Scenic Riverside & Botanical Gardens Excursion", "category": "Relaxation", "neighborhood": "Green Belt", "cost_usd": 8.0, "duration_hours": 2.0, "rating": 4.7, "desc": f"Tranquil walking path through lush gardens and scenic waterfront promenades."},
        {"name": f"{city_name} Local Craft & Artisan Market Safari", "category": "Culture", "neighborhood": "Artisan District", "cost_usd": 0.0, "duration_hours": 2.0, "rating": 4.6, "desc": f"Handcrafted souvenirs, textiles, and authentic local artisan workshops."},
        {"name": f"Twilight Rooftop Lounge & Craft Cocktail Experience", "category": "Nightlife", "neighborhood": "Entertainment Hub", "cost_usd": 38.0, "duration_hours": 2.5, "rating": 4.8, "desc": f"Unwind with signature drinks and ambient music overlooking illuminated landmarks."},
        {"name": f"{city_name} Coastal & Outdoor Day Trip", "category": "Adventure", "neighborhood": "Outskirts", "cost_usd": 45.0, "duration_hours": 4.5, "rating": 4.9, "desc": f"Excursion into surrounding natural wonders, trails, or coastal viewpoints."}
    ]

    return {
        "id": f"dyn-{seed % 10000}",
        "city": city_name,
        "country": country_name,
        "currency": "Local Currency (USD/EUR/FX)",
        "tagline": taglines[seed % len(taglines)],
        "image_url": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&auto=format&fit=crop&q=80",
        "flight_estimate_usd": { "budget": 550, "standard": 850, "premium": 1700 },
        "hotel_estimate_usd_per_night": { "Budget": 75, "Boutique": 160, "Luxury": 420 },
        "daily_food_usd": { "Budget": 30, "Boutique": 70, "Luxury": 160 },
        "neighborhoods": ["Central District", "Old Town", "Waterfront", "Artisan Quarter"],
        "activities": custom_activities
    }

def curate_activities(dest_info: dict, interests: list, pace: str = "Balanced") -> list:
    """
    Curates candidate activities matching user preferences.
    interests: list of string tags ('Food', 'Culture', 'Sightseeing', 'Adventure', 'Relaxation', 'Nightlife')
    pace: 'Relaxed' (2 per day), 'Balanced' (3 per day), 'Action-Packed' (4 per day)
    """
    all_acts = dest_info.get("activities", [])
    if not all_acts:
        return []

    selected_interests = [i.lower() for i in interests] if interests else ["culture", "food", "sightseeing"]
    
    scored_acts = []
    for act in all_acts:
        category = act.get("category", "").lower()
        match_score = 3.0 if any(cat_word in category or category in cat_word for cat_word in selected_interests) else 1.0
        rating_boost = act.get("rating", 4.5) / 5.0
        total_score = match_score + rating_boost
        scored_acts.append((total_score, act))
        
    scored_acts.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored_acts]

