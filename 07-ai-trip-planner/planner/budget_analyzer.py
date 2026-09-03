"""
Budget Intelligence & Financial Variance Engine.
Calculates full financial breakdown, comparison vs stated budget, and cost-saving tips.
"""
import pandas as pd
import numpy as np
import plotly.express as px

def analyze_trip_budget(logistics: dict, itinerary: list, total_budget: float, travelers: int) -> dict:
    """
    Computes total estimated trip cost vs user's target budget.
    """
    flights = logistics.get("total_flights", 0.0)
    hotel = logistics.get("total_hotel", 0.0)
    food = logistics.get("total_food", 0.0)
    
    activities_total = sum(day.get("total_day_cost", 0.0) for day in itinerary)
    subtotal = flights + hotel + food + activities_total
    contingency_buffer = round(subtotal * 0.08, 2) # 8% buffer
    grand_total = round(subtotal + contingency_buffer, 2)
    
    variance = round(total_budget - grand_total, 2)
    variance_pct = round((variance / total_budget) * 100, 1) if total_budget > 0 else 0.0
    
    if variance >= 0:
        status = "Within Budget"
        status_color = "#10b981"
        status_msg = f"🎉 **Great news!** Your estimated trip is **${variance:,.2f} under budget** ({variance_pct:.1f}% buffer remaining)."
    elif abs(variance) <= total_budget * 0.10:
        status = "Near Budget (±10%)"
        status_color = "#f59e0b"
        status_msg = f"⚖️ **Close to Target:** Exceeds target budget slightly by **${abs(variance):,.2f}** ({abs(variance_pct):.1f}% over). Easily manageable with slight dining/lodging tweaks."
    else:
        status = "Over Budget"
        status_color = "#ef4444"
        status_msg = f"⚠️ **Budget Alert:** Trip exceeds target by **${abs(variance):,.2f}** ({abs(variance_pct):.1f}% over). Review cost-saving recommendations below."

    # Breakdown DataFrame
    breakdown_data = [
        {"Category": "✈️ Flights", "Total ($)": round(flights, 2), "Per Person ($)": round(flights / max(1, travelers), 2), "Share %": round(flights / grand_total * 100, 1)},
        {"Category": "🏨 Accommodations", "Total ($)": round(hotel, 2), "Per Person ($)": round(hotel / max(1, travelers), 2), "Share %": round(hotel / grand_total * 100, 1)},
        {"Category": "🍽️ Dining & Food", "Total ($)": round(food, 2), "Per Person ($)": round(food / max(1, travelers), 2), "Share %": round(food / grand_total * 100, 1)},
        {"Category": "🎟️ Activities & Tours", "Total ($)": round(activities_total, 2), "Per Person ($)": round(activities_total / max(1, travelers), 2), "Share %": round(activities_total / grand_total * 100, 1)},
        {"Category": "🛡️ Contingency Buffer", "Total ($)": round(contingency_buffer, 2), "Per Person ($)": round(contingency_buffer / max(1, travelers), 2), "Share %": round(contingency_buffer / grand_total * 100, 1)}
    ]
    df_breakdown = pd.DataFrame(breakdown_data)

    # Cost-saving recommendations
    tips = []
    if variance < 0:
        tips.append("Switch lodging tier from Luxury/Boutique to quality 3-star boutique apartments to save ~30% on lodging.")
        tips.append("Balance fine dining with authentic local food halls, izakayas, and bistros.")
        tips.append("Book flights mid-week (Tuesday/Wednesday departures) to capture 15-20% lower airfare.")
    else:
        tips.append("You have surplus budget! Consider upgrading to a scenic rooftop dinner or private guided excursion.")

    return {
        "grand_total": grand_total,
        "per_person_total": round(grand_total / max(1, travelers), 2),
        "target_budget": total_budget,
        "variance": variance,
        "variance_pct": variance_pct,
        "status": status,
        "status_color": status_color,
        "status_msg": status_msg,
        "breakdown_df": df_breakdown,
        "tips": tips
    }
