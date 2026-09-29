from .marketplaces import choose_platform, search_url

def _item(name, category, price, qty, planner, reason):
    platform = choose_platform(category, planner)
    return {"name": name, "category": category, "estimated_price": price, "quantity": qty,
            "platform": platform, "search_url": search_url(platform, name), "reason": reason}

def home_fallback(data):
    budget = data.budget
    count = len(data.items)
    per = budget / max(count, 1)
    recs = []
    for item in data.items:
        p = max(500, round(per * 0.75 / item.quantity, 0))
        recs.append(_item(f"{data.style.title()} {item.category}", item.category, p, item.quantity, "home",
                          f"A practical {data.style} option sized for {item.quantity} unit(s)."))
    total = sum(x["estimated_price"] * x["quantity"] for x in recs)
    return {"planner":"home","title":"Home Interior Budget Plan","summary":f"A {data.style} starter plan for {', '.join(data.rooms)}.",
            "total_estimated":total,"budget":budget,"budget_remaining":budget-total,
            "allocations":[{"category":"Furniture & decor","amount":budget*0.55,"percentage":55},
                           {"category":"Lighting","amount":budget*0.20,"percentage":20},
                           {"category":"Accessories","amount":budget*0.15,"percentage":15},
                           {"category":"Contingency","amount":budget*0.10,"percentage":10}],
            "recommendations":recs,"tips":["Compare dimensions before ordering.","Keep 5–10% of the budget as contingency.","Use platform links to check current prices before purchase."],"ai_generated":False,
            "warning":"AI is unavailable or not configured; these are deterministic starter recommendations, not live product prices."}

def party_fallback(data):
    budget = data.budget
    allocations=[("Food & catering",.45), ("Venue",.25), ("Decoration",.15), ("Entertainment",.10), ("Contingency",.05)]
    recs=[
        _item(f"{data.event_type.title()} catering package", "Food & catering", budget*.45/max(data.guests,1), data.guests, "party", "Budget-aware food allowance per guest."),
        _item(f"{data.venue} event venue", "Venue", budget*.25, 1, "party", "Venue allowance sized to the total event budget."),
        _item(f"{data.event_type.title()} decoration package", "Decoration", budget*.15, 1, "party", "Basic decor allocation suitable for the selected event type."),
    ]
    total=sum(x["estimated_price"]*x["quantity"] for x in recs)
    return {"planner":"party","title":"Party Budget Plan","summary":f"A starting plan for {data.guests} guests at a {data.event_type} event.",
            "total_estimated":total,"budget":budget,"budget_remaining":budget-total,
            "allocations":[{"category":c,"amount":budget*p,"percentage":p*100} for c,p in allocations],
            "recommendations":recs,"tips":["Confirm per-person food pricing directly with the vendor.","Reserve the venue before finalizing decor spend.","Keep a contingency amount for last-minute guests or services."],"ai_generated":False,
            "warning":"AI is unavailable or not configured; vendor prices are estimates only."}

def jewelry_fallback(data):
    budget=data.budget
    recs=[
        _item(f"{data.style.title()} {data.metal.title()} necklace", "Necklace", budget*.35, 1, "jewelry", f"Designed for a {data.occasion} occasion."),
        _item(f"{data.style.title()} {data.metal.title()} earrings", "Earrings", budget*.25, 1, "jewelry", "Balances the necklace without consuming the full budget."),
        _item(f"{data.style.title()} bracelet", "Bracelet", budget*.15, 1, "jewelry", "Optional coordinating accent."),
    ]
    total=sum(x["estimated_price"] for x in recs)
    return {"planner":"jewelry","title":"Jewelry Budget Plan","summary":f"A {data.style} selection for {data.occasion} within your budget.",
            "total_estimated":total,"budget":budget,"budget_remaining":budget-total,
            "allocations":[{"category":"Necklace","amount":budget*.35,"percentage":35},{"category":"Earrings","amount":budget*.25,"percentage":25},{"category":"Bracelet","amount":budget*.15,"percentage":15},{"category":"Reserve","amount":budget*.25,"percentage":25}],
            "recommendations":recs,"tips":["Match metal tone with the outfit hardware where possible.","For a heavily embellished outfit, consider simpler jewelry.","Verify material, dimensions, return policy, and seller rating before purchase."],"ai_generated":False,
            "warning":"AI/image analysis is unavailable or not configured; these are style-based starter suggestions."}
