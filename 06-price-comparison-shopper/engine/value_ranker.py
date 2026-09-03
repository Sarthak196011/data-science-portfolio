"""
Value Scoring & Retailer Comparison Ranker.
Ranks deals by price-to-rating value ratio, shipping advantages, and trust metrics.
"""
import pandas as pd
import numpy as np

def compute_value_scores(stores: list) -> list:
    """
    Computes a 0-100 Value Score for each retailer offer:
    Value Score = Price Efficiency (60%) + Store Trust & Rating (30%) + Shipping Convenience (10%)
    """
    if not stores:
        return []

    prices = [s["price"] + s.get("shipping", 0.0) for s in stores]
    min_p = min(prices)
    max_p = max(prices)
    p_range = (max_p - min_p) if max_p > min_p else 1.0

    scored_stores = []
    for s in stores:
        total_cost = s["price"] + s.get("shipping", 0.0)
        
        # Price score: 100 for lowest price, drops as price rises
        price_efficiency = 100.0 - ((total_cost - min_p) / p_range * 60.0)
        
        # Rating score
        rating = s.get("rating", 4.0)
        rating_score = (rating / 5.0) * 30.0
        
        # Shipping score
        ship_score = 10.0 if s.get("shipping", 0.0) == 0.0 else 5.0
        
        total_value = int(np.clip(round(price_efficiency + rating_score + ship_score), 10, 100))
        
        store_copy = dict(s)
        store_copy["total_cost"] = round(total_cost, 2)
        store_copy["value_score"] = total_value
        scored_stores.append(store_copy)

    # Sort descending by value score
    scored_stores.sort(key=lambda x: x["value_score"], reverse=True)
    return scored_stores
