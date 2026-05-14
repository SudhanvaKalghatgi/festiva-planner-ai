def negotiation_agent(plan_data):
    parsed = plan_data.get("parsed_input", {})
    budget = plan_data.get("budget_split", {})

    negotiation_points = []

    city = parsed.get("city", "").lower()
    guests = parsed.get("guest_count", 0)
    total_budget = parsed.get("budget", 0)
    is_destination = parsed.get("is_destination", 0)

    # -----------------------------------
    # 🔥 Catering Negotiation
    # -----------------------------------
    catering_amount = budget.get(
        "catering", {}
    ).get("amount", 0)

    if guests > 0:
        per_plate = catering_amount / guests

        target_low = int(per_plate * 0.85)
        target_high = int(per_plate * 0.95)

        negotiation_points.append(
            f"Start catering negotiation around "
            f"₹{target_low}–₹{target_high} per guest."
        )

        if guests >= 150:
            negotiation_points.append(
                "Use large guest count as leverage for bulk discounts."
            )

    # -----------------------------------
    # 🔥 Venue Negotiation
    # -----------------------------------
    venue_amount = budget.get(
        "venue", {}
    ).get("amount", 0)

    if venue_amount > 0:
        negotiation_points.append(
            "Ask venues for bundled packages including decor or lighting services."
        )

    # -----------------------------------
    # 🔥 Destination Wedding Logic
    # -----------------------------------
    if is_destination:
        negotiation_points.append(
            "Negotiate group booking discounts for hotels and guest accommodations."
        )

        negotiation_points.append(
            "Request complimentary airport or local transport services."
        )

    # -----------------------------------
    # 🔥 High-Demand Cities
    # -----------------------------------
    high_demand_cities = [
        "bangalore",
        "mumbai",
        "delhi"
    ]

    if city in high_demand_cities:
        negotiation_points.append(
            "Weekday bookings may significantly reduce venue pricing."
        )

    # -----------------------------------
    # 🔥 Budget-Based Strategy
    # -----------------------------------
    if total_budget < 800000:
        negotiation_points.append(
            "Focus negotiations on essential services before luxury add-ons."
        )

    elif total_budget > 3000000:
        negotiation_points.append(
            "Premium budgets provide leverage for complimentary upgrades and premium inclusions."
        )

    # -----------------------------------
    # 🔥 Payment Safety
    # -----------------------------------
    negotiation_points.append(
        "Avoid paying more than 30–40% advance before vendor confirmation."
    )

    negotiation_points.append(
        "Request written quotations to avoid hidden charges later."
    )

    # -----------------------------------
    # 🔥 Remove duplicates
    # -----------------------------------
    negotiation_points = list(
        dict.fromkeys(negotiation_points)
    )

    return negotiation_points