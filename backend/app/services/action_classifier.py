from .direction_classifier import classify_direction

def classify_action_plan(raw_text: str, important_sentences: list[str], extracted_entities: dict) -> dict:
    best_direction = None
    best_score = -1
    
    for sentence in important_sentences:
        classified = classify_direction(sentence)
        if classified["score"] > best_score:
            best_score = classified["score"]
            best_direction = classified
            
    if not best_direction:
        best_direction = {
            "label": "MANUAL_REVIEW",
            "matched_keywords": [],
            "score": 40,
            "sentence": ""
        }
        
    label_to_action = {
        "COMPLIANCE_DIRECTION": "Compliance",
        "REPORT_SUBMISSION": "Report Submission",
        "APPEAL_REVIEW": "Appeal Review",
        "NOTICE_OR_HEARING": "Hearing / Notice Follow-up",
        "MANUAL_REVIEW": "Manual Review"
    }
    
    action_type = label_to_action.get(best_direction["label"], "Manual Review")
    deadline = extracted_entities.get("timeline", "No explicit deadline detected")
    dept = extracted_entities.get("responsible_department", "Department requires manual verification")
    
    # Priority logic
    priority = "Medium"
    if action_type == "Appeal Review":
        priority = "High"
    elif deadline != "No explicit deadline detected":
        priority = "High"
    elif action_type == "Report Submission":
        priority = "High"
    elif action_type == "Manual Review":
        priority = "Medium"
        
    # Required action examples
    if action_type == "Compliance":
        required_action = "The responsible department must comply with the court direction and complete the required action within the detected deadline."
    elif action_type == "Report Submission":
        required_action = "The department must prepare and submit the required compliance/status report."
    elif action_type == "Appeal Review":
        required_action = "The legal team must review the judgment for appeal possibility and limitation period."
    elif action_type == "Hearing / Notice Follow-up":
        required_action = "The concerned team must follow up on the notice or prepare for the next hearing."
    else:
        required_action = "The judgment requires manual legal review because clear action direction was not confidently detected."
        
    reason = f"Classified based on keywords: {', '.join(best_direction['matched_keywords'])}" if best_direction["matched_keywords"] else "No specific keywords matched."
    
    return {
        "action_type": action_type,
        "required_action": required_action,
        "responsible_department": dept,
        "deadline": deadline,
        "priority": priority,
        "risk_level": "Medium", # Will be overwritten by risk_service
        "reason": reason,
        "source_text": best_direction["sentence"],
        "classification_score": best_direction["score"]
    }
