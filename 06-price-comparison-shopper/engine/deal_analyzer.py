"""
Deal Intelligence & Statistical Price Analysis Engine.
Calculates Deal Score (0-100), 90-day median variance, and fake discount detection.
"""
import numpy as np
import pandas as pd

def analyze_deal(product: dict) -> dict:
    """
    Perform deep statistical analysis on product pricing.
    Returns {
        current_best_price,
        best_store,
        median_90d,
        lowest_90d,
        highest_90d,
        deal_score (0-100),
        discount_vs_median_pct,
        discount_vs_competitor_pct,
        is_fake_deal,
        deal_verdict_badge,
        verdict_explanation,
        history_df,
        comparison_df
    }
    """
    stores = product.get("stores", [])
    if not stores:
        return {}

    # Sort stores by total price (price + shipping)
    stores_sorted = sorted(stores, key=lambda s: s["price"] + s.get("shipping", 0.0))
    best_store_info = stores_sorted[0]
    best_price = best_store_info["price"]
    best_store_name = best_store_info["store"]

    # Historical 90-day metrics
    history = product.get("history_90d", {"dates": [], "prices": []})
    hist_prices = history.get("prices", [best_price])
    hist_dates = history.get("dates", [])
    
    median_90d = float(np.median(hist_prices))
    lowest_90d = float(np.min(hist_prices))
    highest_90d = float(np.max(hist_prices))
    
    # Competitor average (excluding the lowest price)
    competitor_prices = [s["price"] for s in stores if s["store"] != best_store_name]
    avg_competitor_price = float(np.mean(competitor_prices)) if competitor_prices else best_price
    
    # Discount vs 90-day median
    discount_vs_median_pct = ((median_90d - best_price) / median_90d) * 100 if median_90d > 0 else 0.0
    
    # Discount vs competitor average
    discount_vs_comp_pct = ((avg_competitor_price - best_price) / avg_competitor_price) * 100 if avg_competitor_price > 0 else 0.0
    
    # Discount vs MSRP
    msrp = product.get("msrp", median_90d)
    discount_vs_msrp = ((msrp - best_price) / msrp) * 100 if msrp > 0 else 0.0

    # ── Deal Score Algorithm (0 to 100) ───────────────────────────────────────
    # Component 1: Historical discount score (50%)
    if best_price <= lowest_90d:
        hist_score = 50.0
    elif discount_vs_median_pct > 0:
        hist_score = 25.0 + min(25.0, discount_vs_median_pct * 1.5)
    else:
        hist_score = max(0.0, 25.0 + discount_vs_median_pct)
        
    # Component 2: Competitor discount score (30%)
    comp_score = min(30.0, max(0.0, 15.0 + (discount_vs_comp_pct * 1.2)))
    
    # Component 3: Store reliability & in-stock bonus (20%)
    rating_score = (best_store_info.get("rating", 4.5) / 5.0) * 15.0
    stock_bonus = 5.0 if best_store_info.get("in_stock", True) else 0.0
    
    deal_score = int(np.clip(round(hist_score + comp_score + rating_score + stock_bonus), 0, 100))

    # ── Fake Deal / Inflated MSRP Detection ───────────────────────────────────
    # If the claimed original price is way above the actual 90-day median
    claimed_original = best_store_info.get("original_price", msrp)
    is_fake_deal = False
    fake_deal_reason = ""
    
    if claimed_original > median_90d * 1.25 and best_price >= median_90d * 0.96:
        is_fake_deal = True
        fake_deal_reason = f"Advertised original price (${claimed_original:,.2f}) is inflated. True 90-day median is ${median_90d:,.2f}."

    # ── Verdict Classification ────────────────────────────────────────────────
    if deal_score >= 85:
        verdict_badge = "🔥 Excellent Deal (All-Time Low)"
        verdict_color = "#10b981"
        action = "BUY NOW"
    elif deal_score >= 70:
        verdict_badge = "✅ Good Deal"
        verdict_color = "#3b82f6"
        action = "FAVORABLE BUY"
    elif deal_score >= 50:
        verdict_badge = "⚖️ Fair Market Price"
        verdict_color = "#f59e0b"
        action = "NEUTRAL"
    else:
        verdict_badge = "⚠️ Overpriced / Wait for Sale"
        verdict_color = "#ef4444"
        action = "WAIT"

    # Narrative explanation
    if is_fake_deal:
        explanation = f"⚠️ **Artificial Sale Warning:** {fake_deal_reason} The current ${best_price:,.2f} price is essentially the standard market rate."
    elif discount_vs_median_pct >= 15:
        explanation = f"🔥 **Verified Real Deal:** Current price is **{discount_vs_median_pct:.1f}% below the 90-day median** (${median_90d:,.2f}) and saves you **${(avg_competitor_price - best_price):,.2f}** compared to other retailers."
    elif discount_vs_median_pct > 0:
        explanation = f"✅ **Modest Discount:** Currently **{discount_vs_median_pct:.1f}% under normal median**. It is **${(avg_competitor_price - best_price):,.2f} cheaper** than the competitor average."
    else:
        explanation = f"⏳ **Above Typical Price:** Current price is **{abs(discount_vs_median_pct):.1f}% higher** than the 90-day median (${median_90d:,.2f}). We recommend waiting for the next seasonal price drop."

    # Comparison DataFrame
    comp_rows = []
    for s in stores_sorted:
        total_p = s["price"] + s.get("shipping", 0.0)
        diff_from_best = total_p - (best_price + best_store_info.get("shipping", 0.0))
        comp_rows.append({
            "Retailer": s["store"],
            "Price ($)": s["price"],
            "Shipping ($)": s.get("shipping", 0.0),
            "Total ($)": round(total_p, 2),
            "Difference": "Best Price" if diff_from_best == 0 else f"+${diff_from_best:,.2f}",
            "Store Rating": s.get("rating", "—"),
            "Stock Status": "In Stock" if s.get("in_stock", True) else "Out of Stock",
            "Special Tag": s.get("badge", "—"),
            "Direct Link": s.get("url", "#")
        })
    comparison_df = pd.DataFrame(comp_rows)

    # History DataFrame
    history_df = pd.DataFrame({
        "Date": pd.to_datetime(hist_dates),
        "Price": hist_prices
    }).sort_values("Date")

    return {
        "best_price": best_price,
        "best_store": best_store_name,
        "best_store_url": best_store_info.get("url", "#"),
        "median_90d": median_90d,
        "lowest_90d": lowest_90d,
        "highest_90d": highest_90d,
        "deal_score": deal_score,
        "discount_vs_median_pct": round(discount_vs_median_pct, 1),
        "discount_vs_comp_pct": round(discount_vs_comp_pct, 1),
        "discount_vs_msrp": round(discount_vs_msrp, 1),
        "savings_vs_avg": round(avg_competitor_price - best_price, 2),
        "is_fake_deal": is_fake_deal,
        "verdict_badge": verdict_badge,
        "verdict_color": verdict_color,
        "action": action,
        "explanation": explanation,
        "comparison_df": comparison_df,
        "history_df": history_df
    }
