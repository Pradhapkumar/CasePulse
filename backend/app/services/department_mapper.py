def map_department(text: str) -> str:
    text_lower = text.lower()
    if any(k in text_lower for k in ["revenue", "land", "tahsildar", "deputy commissioner"]):
        return "Revenue Department"
    elif any(k in text_lower for k in ["police", "fir", "investigation"]):
        return "Police Department"
    elif any(k in text_lower for k in ["education", "school", "college"]):
        return "Education Department"
    elif any(k in text_lower for k in ["health", "hospital", "medical"]):
        return "Health Department"
    elif any(k in text_lower for k in ["municipality", "municipal", "corporation", "panchayat"]):
        return "Urban Development Department"
    elif any(k in text_lower for k in ["labour", "employee", "worker"]):
        return "Labour Department"
    elif any(k in text_lower for k in ["transport", "vehicle", "license"]):
        return "Transport Department"
    return "Department requires manual verification"
