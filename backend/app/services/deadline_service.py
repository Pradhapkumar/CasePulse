def detect_deadline(text: str) -> str:
    text_lower = text.lower()
    deadlines = [
        "within 30 days", "within 60 days", "within four weeks", "within two months",
        "30 days", "60 days", "4 weeks", "2 months"
    ]
    for d in deadlines:
        if d in text_lower:
            return d
    return "No explicit deadline detected"
