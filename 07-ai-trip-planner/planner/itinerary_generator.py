"""
Day-by-Day Itinerary Generation & Single-Day Regeneration Engine.
Constructs neighborhood-clustered daily plans (Morning, Afternoon, Evening) with travel narratives.
"""
import numpy as np

def generate_itinerary(dest_info: dict, candidate_activities: list, days: int, travelers: int, pace: str = "Balanced") -> list:
    """
    Generates structured multi-day itinerary.
    Returns a list of day dicts:
    [
      {
        "day_num": 1,
        "theme": "Arrival & Historic Discovery",
        "neighborhood": "Asakusa",
        "morning": {...},
        "afternoon": {...},
        "evening": {...},
        "day_cost": 45.0,
        "narrative": "..."
      },
      ...
    ]
    """
    if not candidate_activities:
        candidate_activities = dest_info.get("activities", [])
        
    num_acts_per_day = 2 if pace == "Relaxed" else (3 if pace == "Balanced" else 4)
    itinerary = []
    
    act_pool = list(candidate_activities)
    # If not enough activities, cycle with variations
    while len(act_pool) < days * 3:
        act_pool.extend(candidate_activities)

    for d in range(1, days + 1):
        day_plan = _build_single_day(d, act_pool, dest_info, travelers, num_acts_per_day)
        itinerary.append(day_plan)

    return itinerary

def regenerate_single_day(dest_info: dict, current_itinerary: list, day_to_regen: int, travelers: int, pace: str = "Balanced") -> list:
    """
    Regenerates only one specified day in the itinerary while preserving all other days intact.
    """
    all_acts = dest_info.get("activities", [])
    num_acts = 2 if pace == "Relaxed" else (3 if pace == "Balanced" else 4)
    
    # Shuffle activity pool for fresh selection
    shuffled_pool = list(all_acts)
    np.random.shuffle(shuffled_pool)
    
    new_day = _build_single_day(day_to_regen, shuffled_pool, dest_info, travelers, num_acts)
    
    updated_itinerary = []
    for day in current_itinerary:
        if day["day_num"] == day_to_regen:
            updated_itinerary.append(new_day)
        else:
            updated_itinerary.append(day)
            
    return updated_itinerary

def _build_single_day(day_num: int, act_pool: list, dest_info: dict, travelers: int, num_acts: int) -> dict:
    city = dest_info.get("city", "Destination")
    
    # Slice items for morning, afternoon, evening
    start_idx = ((day_num - 1) * 3) % max(1, len(act_pool) - 2)
    m_act = act_pool[start_idx % len(act_pool)]
    a_act = act_pool[(start_idx + 1) % len(act_pool)]
    e_act = act_pool[(start_idx + 2) % len(act_pool)]
    
    day_acts = [m_act, a_act, e_act][:num_acts]
    total_day_activity_cost = sum(a.get("cost_usd", 0) for a in day_acts) * travelers
    primary_hood = m_act.get("neighborhood", city)

    themes = [
        "Arrival & Historic Landmarks",
        "Culinary Sensations & Street Markets",
        "Panoramic Views & Modern Culture",
        "Art, Museums & Scenic Strolls",
        "Hidden Gems & Local Nightlife",
        "Nature Escape & Outdoor Discovery",
        "Relaxation, Shopping & Farewell Dinner"
    ]
    theme = themes[(day_num - 1) % len(themes)]

    narrative = (
        f"**Day {day_num} in {city} — {theme}:** Begin your morning in **{m_act.get('neighborhood', primary_hood)}** "
        f"visiting **{m_act['name']}** ({m_act.get('desc', '')}). In the afternoon, head over to **{a_act['name']}** "
        f"to experience {a_act.get('category', 'local culture').lower()}. Wrap up the evening with **{e_act['name']}** "
        f"enjoying {e_act.get('desc', 'local evening atmosphere')}."
    )

    return {
        "day_num": day_num,
        "theme": theme,
        "neighborhood": primary_hood,
        "morning": m_act,
        "afternoon": a_act,
        "evening": e_act if num_acts >= 3 else None,
        "activities": day_acts,
        "day_cost_per_person": sum(a.get("cost_usd", 0) for a in day_acts),
        "total_day_cost": total_day_activity_cost,
        "narrative": narrative
    }
