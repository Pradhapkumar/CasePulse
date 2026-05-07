def calculate_compliance_risk(action_type: str, deadline: str, confidence: int, source_text: str) -> dict:
    risk_score = 30
    risk_factors = []
    
    # Handle potential None inputs
    action_type = action_type or "Unknown"
    deadline = deadline or "No explicit deadline detected"
    confidence = confidence if confidence is not None else 0
    source_text = source_text or ""
    
    if deadline != "No explicit deadline detected":
        risk_score += 30
        risk_factors.append("Time-bound court direction detected")
        
    if action_type == "Appeal Review":
        risk_score += 25
        risk_factors.append("Appeal limitation period risk")
    elif action_type == "Report Submission":
        risk_score += 20
        risk_factors.append("Compliance report required")
        
    if "shall" in source_text.lower() or "directed" in source_text.lower():
        risk_score += 20
        risk_factors.append("Mandatory compliance language detected")
        
    if confidence < 60:
        risk_score += 15
        risk_factors.append("Low AI confidence requires careful manual review")
        
    # Department requires manual verification check is typically handled before calling this, but we can infer from confidence if needed
    
    risk_score = min(risk_score, 100)
    
    if risk_score >= 75:
        risk_level = "High"
    elif risk_score >= 45:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors
    }
