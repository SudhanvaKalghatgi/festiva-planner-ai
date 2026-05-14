from src.agents.polish_agent import polish_response


def format_budget(plan_data):
    budget = plan_data.get("budget_split", {})
    lines = ["📊 Budget Breakdown:\n"]

    for category, data in budget.items():
        pct = data["percentage"] * 100
        amt = data["amount"]

        lines.append(
            f"- {category.capitalize()}: ₹{amt:,} ({pct:.1f}%)"
        )

    return "\n".join(lines)


def format_summary(plan_data):
    parsed = plan_data.get("parsed_input", {})

    return (
        "📌 Event Summary:\n"
        f"- Event: {parsed.get('event_type', '').capitalize()}\n"
        f"- City: {parsed.get('city', '').capitalize()}\n"
        f"- Guests: {parsed.get('guest_count')}\n"
        f"- Budget: ₹{parsed.get('budget'):,}\n"
    )


def format_knowledge(knowledge_data):
    if not knowledge_data:
        return ""

    answer = knowledge_data.get("answer", "")

    return f"📚 Planning Guidance:\n\n{answer}"


def format_recommendations(recommendations):
    if not recommendations:
        return ""

    lines = ["🎯 Smart Recommendations:\n"]

    for recommendation in recommendations:
        lines.append(f"- {recommendation}")

    return "\n".join(lines)


def format_negotiation(negotiation):
    if not negotiation:
        return ""

    lines = ["💬 Negotiation Strategy:\n"]

    for item in negotiation:
        lines.append(f"- {item}")

    return "\n".join(lines)


def generate_insights(plan_data):
    budget = plan_data.get("budget_split", {})
    insights = []

    if not budget:
        return ""

    # 🔥 Ignore contingency for main analysis
    filtered_budget = {
        k: v for k, v in budget.items()
        if k != "contingency"
    }

    max_category = max(
        filtered_budget,
        key=lambda x: filtered_budget[x]["amount"]
    )

    max_value = filtered_budget[max_category]["amount"]

    insights.append(
        f"💡 Highest spending is on "
        f"{max_category.capitalize()} "
        f"(₹{max_value:,}). "
        f"Consider optimizing this category."
    )

    # 🔥 Contingency logic
    contingency = budget.get(
        "contingency", {}
    ).get("percentage", 0)

    if contingency > 0.15:
        insights.append(
            "⚠️ Contingency fund is high (>15%). "
            "You may reallocate some budget if risk is low."
        )

    elif contingency < 0.08:
        insights.append(
            "⚠️ Contingency fund is low (<8%). "
            "Consider increasing it to handle unexpected expenses."
        )

    else:
        insights.append(
            "✅ Contingency allocation looks balanced."
        )

    # 🔥 Catering analysis
    catering_pct = budget.get(
        "catering", {}
    ).get("percentage", 0)

    if catering_pct > 0.18:
        insights.append(
            "💡 Catering cost is high. "
            "Try negotiating per plate pricing."
        )

    elif catering_pct < 0.10:
        insights.append(
            "⚠️ Catering allocation is low. "
            "Guest experience may be affected."
        )

    # 🔥 Venue analysis
    venue_pct = budget.get(
        "venue", {}
    ).get("percentage", 0)

    if venue_pct > 0.20:
        insights.append(
            "💡 Venue cost is high. "
            "Consider alternative venues or off-season booking."
        )

    elif venue_pct < 0.08:
        insights.append(
            "⚠️ Venue allocation looks low. "
            "Finding quality venues may be difficult."
        )

    # 🔥 Decor analysis
    decor_pct = budget.get(
        "decor", {}
    ).get("percentage", 0)

    if decor_pct > 0.18:
        insights.append(
            "💡 Decor spending is relatively high. "
            "Consider reallocating some budget toward guest experience."
        )

    return "\n".join(insights)


def generate_final_output(response: dict):
    plan = response.get("plan")
    knowledge = response.get("knowledge")
    conflicts = response.get("conflicts")
    recommendations = response.get("recommendations")
    negotiation = response.get("negotiation")

    sections = []

    # 🔥 Plan section
    if plan:
        sections.append(format_summary(plan))
        sections.append(format_budget(plan))

        insights = generate_insights(plan)

        if insights:
            sections.append(
                "💡 Key Insights & Recommendations:\n\n"
                + insights
            )

    # 🔥 Conflict warnings
    if conflicts:
        warnings_text = "\n".join(
            [f"- {warning}" for warning in conflicts]
        )

        sections.append(
            "🚨 Risks & Warnings:\n\n"
            + warnings_text
        )

    # 🔥 Recommendations
    if recommendations:
        sections.append(
            format_recommendations(recommendations)
        )

    # 🔥 Negotiation section
    if negotiation:
        sections.append(
            format_negotiation(negotiation)
        )

    # 🔥 Knowledge section
    if knowledge:
        sections.append(
            format_knowledge(knowledge)
        )

    final_output = "\n\n".join(sections)

    # 🔥 LLM polishing
    try:
        if len(final_output) > 200:

            polished = polish_response(final_output)

            if polished and len(polished.strip()) > 0:
                final_output = polished

    except Exception:
        pass  # silent fallback

    return {
        "formatted_response": final_output,
        "raw": response
    }