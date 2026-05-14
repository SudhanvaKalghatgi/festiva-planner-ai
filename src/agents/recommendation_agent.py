def recommendation_agent(plan_data, conflicts):
    parsed = plan_data.get("parsed_input", {})
    budget = plan_data.get("budget_split", {})

    recommendations = []

    guests = parsed.get("guest_count", 0)
    total_budget = parsed.get("budget", 0)
    city = parsed.get("city", "").lower()
    is_destination = parsed.get("is_destination", 0)

    # -----------------------------------
    # 🔥 Budget Per Guest Analysis
    # -----------------------------------
    if guests > 0:
        per_guest = total_budget / guests

        if per_guest < 3000:
            recommendations.append(
                "Reduce guest count or increase overall budget to maintain event quality."
            )

            recommendations.append(
                "Prioritize catering and venue over luxury decor and entertainment."
            )

        elif per_guest > 15000:
            recommendations.append(
                "You have strong budget flexibility. Consider enhancing guest experience with premium services."
            )

    # -----------------------------------
    # 🔥 Catering Recommendations
    # -----------------------------------
    catering_pct = budget.get("catering", {}).get("percentage", 0)

    if catering_pct < 0.10:
        recommendations.append(
            "Increase catering allocation to improve guest satisfaction and food quality."
        )

    elif catering_pct > 0.20:
        recommendations.append(
            "Catering allocation is high. Negotiate per plate pricing or simplify menu options."
        )

    # -----------------------------------
    # 🔥 Decor Recommendations
    # -----------------------------------
    decor_pct = budget.get("decor", {}).get("percentage", 0)

    if decor_pct > 0.18:
        recommendations.append(
            "Consider reducing decor spending and reallocating budget toward guest experience."
        )

    # -----------------------------------
    # 🔥 Venue Recommendations
    # -----------------------------------
    venue_pct = budget.get("venue", {}).get("percentage", 0)

    if venue_pct > 0.25:
        recommendations.append(
            "Venue allocation is very high. Consider alternative venues or off-season booking discounts."
        )

    # -----------------------------------
    # 🔥 Destination Wedding Logic
    # -----------------------------------
    if is_destination:
        recommendations.append(
            "Book vendors and accommodations early to avoid seasonal price surges."
        )

        recommendations.append(
            "Plan buffer budget for travel, logistics, and unexpected destination costs."
        )

    # -----------------------------------
    # 🔥 City-Specific Logic
    # -----------------------------------
    high_demand_cities = ["bangalore", "mumbai", "delhi"]

    if city in high_demand_cities:
        recommendations.append(
            "Consider weekday bookings to reduce venue and vendor costs in high-demand cities."
        )

    # -----------------------------------
    # 🔥 Conflict-Based Recommendations
    # -----------------------------------
    for warning in conflicts:

        if "lead time" in warning.lower():
            recommendations.append(
                "Short timelines require immediate vendor booking and simplified planning."
            )

        if "budget" in warning.lower():
            recommendations.append(
                "Focus spending on essentials first before allocating budget to luxury additions."
            )

    # -----------------------------------
    # 🔥 Remove duplicates
    # -----------------------------------
    recommendations = list(dict.fromkeys(recommendations))

    return recommendations