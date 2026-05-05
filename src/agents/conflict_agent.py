def conflict_agent(plan_data):
    parsed = plan_data.get("parsed_input", {})
    budget = plan_data.get("budget_split", {})

    warnings = []

    guests = parsed.get("guest_count", 0)
    total_budget = parsed.get("budget", 0)
    lead_time = parsed.get("lead_time_days", 0)
    city_tier = parsed.get("city_tier", 2)
    is_destination = parsed.get("is_destination", 0)

    # 🔥 Budget per guest analysis
    if guests > 0:
        per_guest = total_budget / guests

        if per_guest < 3000:
            warnings.append(
                "⚠️ Budget per guest is very low (<₹3000). This may affect catering quality and guest experience."
            )
        elif per_guest > 20000:
            warnings.append(
                "⚠️ Budget per guest is extremely high. This may indicate over-allocation. Consider optimizing vendors and costs."
            )
        elif per_guest > 15000:
            warnings.append(
                "💡 Budget per guest is high. You may optimize costs without affecting quality."
            )

    # 🔥 Overall budget feasibility
    if total_budget < 700000 and guests >= 150:
        warnings.append(
            "⚠️ Overall budget is very tight for the number of guests. Consider reducing guest count or increasing budget."
        )

    # 🔥 Lead time risk
    if lead_time < 60:
        warnings.append(
            "⚠️ Lead time is short (<60 days). Vendor availability and pricing may be an issue."
        )

    # 🔥 Destination-aware city demand logic (UPDATED)
    if is_destination:
        if lead_time <= 120:
            warnings.append(
                "⚠️ Destination wedding locations have high demand. Venues and vendors should be booked 4–6 months in advance."
            )

    elif city_tier == 1 and lead_time <= 120:
        warnings.append(
            "⚠️ High-demand city. Venues get booked 3–4 months in advance. Consider booking immediately."
        )

    elif city_tier == 2 and lead_time <= 90:
        warnings.append(
            "⚠️ Moderate-demand city. Early booking is recommended to avoid limited options."
        )

    elif city_tier == 3 and lead_time <= 60:
        warnings.append(
            "💡 Lower-demand city. Booking flexibility is higher, but early planning is still beneficial."
        )

    # 🔥 Catering allocation check
    catering_pct = budget.get("catering", {}).get("percentage", 0)
    if catering_pct < 0.1:
        warnings.append(
            "⚠️ Catering allocation is too low. Guest experience may suffer."
        )

    # 🔥 Decor over-allocation
    decor_pct = budget.get("decor", {}).get("percentage", 0)
    if decor_pct > 0.2:
        warnings.append(
            "💡 Decor allocation is high. Consider reallocating budget to catering or experience."
        )

    # 🔥 Venue realism check
    venue_pct = budget.get("venue", {}).get("percentage", 0)
    if venue_pct < 0.08:
        warnings.append(
            "⚠️ Venue allocation seems low. Finding a good venue may be difficult."
        )

    return warnings