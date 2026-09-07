"""Budget Matrix Calculation Service"""
from typing import Dict, Any

def calculate_budget_matrix(flight_price: int, base_lodging: int, base_exp: int,
                            travel_class: str, days: int) -> Dict[str, Any]:
    """Calculate comprehensive cost breakdown across tiers and duration."""
    lodging_mult = 1.55
    exp_mult = 1.4

    if travel_class.lower() == "economy":
        lodging_mult = 1.0
        exp_mult = 1.0
    elif travel_class.lower() == "first":
        lodging_mult = 2.6
        exp_mult = 2.2

    lodging_nightly = round(base_lodging * lodging_mult)
    total_lodging = lodging_nightly * days
    daily_exp = round(base_exp * exp_mult)
    total_exp = daily_exp * days

    flight_and_stay = flight_price + total_lodging
    total_budget = flight_and_stay + total_exp

    raw = {
        "flight_price": flight_price,
        "lodging_nightly": lodging_nightly,
        "lodging_total": total_lodging,
        "daily_expenses": daily_exp,
        "total_expenses": total_exp,
        "flight_and_stay": flight_and_stay,
        "total_budget": total_budget
    }

    formatted = {
        "flight_price": f"${flight_price:,}",
        "lodging_nightly": f"${lodging_nightly:,}",
        "lodging_total": f"${total_lodging:,}",
        "daily_expenses": f"${daily_exp:,}",
        "total_expenses": f"${total_exp:,}",
        "flight_and_stay": f"${flight_and_stay:,}",
        "total_budget": f"${total_budget:,}"
    }

    return {"raw": raw, "formatted": formatted}
