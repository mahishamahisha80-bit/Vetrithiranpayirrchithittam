from urllib.parse import quote_plus

PLATFORMS = {
    "Amazon": "https://www.amazon.in/s?k={q}",
    "Flipkart": "https://www.flipkart.com/search?q={q}",
    "IKEA": "https://www.ikea.com/in/en/search/?q={q}",
    "Swiggy": "https://www.swiggy.com/search?query={q}",
    "Zomato": "https://www.zomato.com/search?q={q}",
    "OYO": "https://www.oyorooms.com/search?q={q}",
}

def search_url(platform: str, query: str) -> str:
    template = PLATFORMS.get(platform, PLATFORMS["Amazon"])
    return template.format(q=quote_plus(query))

def choose_platform(category: str, planner: str) -> str:
    c = category.lower()
    if planner == "party":
        if any(x in c for x in ("food", "catering", "cake")):
            return "Swiggy"
        if "venue" in c or "hotel" in c or "stay" in c:
            return "OYO"
        return "Zomato"
    if planner == "home" and any(x in c for x in ("furniture", "table", "chair", "storage")):
        return "IKEA"
    return "Amazon"
