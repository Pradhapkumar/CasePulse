def calculate_ai_confidence(extracted_entities: dict, classified_action: dict, source_snippets: list) -> dict:
    entity_confidence = 0
    if extracted_entities.get("case_number"): entity_confidence += 15
    if extracted_entities.get("court_name"): entity_confidence += 15
    if extracted_entities.get("date_of_order"): entity_confidence += 15
    if extracted_entities.get("petitioner") != "Petitioner not clearly detected" or \
       extracted_entities.get("respondent") != "Respondent not clearly detected":
        entity_confidence += 15
    if extracted_entities.get("responsible_department") != "Department requires manual verification":
        entity_confidence += 20
    if extracted_entities.get("timeline") != "No explicit deadline detected":
        entity_confidence += 20
        
    entity_confidence = min(entity_confidence, 100)
    
    action_confidence = classified_action.get("classification_score", 40)
    
    evidence_confidence = 0
    if source_snippets and len(source_snippets) > 0 and source_snippets[0].strip() != "":
        evidence_confidence += 40
        snippet_text = " ".join(source_snippets).lower()
        if any(kw in snippet_text for kw in ["directed to", "shall", "comply", "submit", "appeal", "dispose"]):
            evidence_confidence += 30
        if any(kw in snippet_text for kw in ["within", "days", "weeks", "months", "department"]):
            evidence_confidence += 30
            
    evidence_confidence = min(evidence_confidence, 100)
    
    overall_confidence = int((entity_confidence + action_confidence + evidence_confidence) / 3)
    
    if overall_confidence >= 80:
        confidence_level = "High"
    elif overall_confidence >= 50:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"
        
    return {
        "overall_confidence": overall_confidence,
        "entity_confidence": entity_confidence,
        "action_confidence": action_confidence,
        "evidence_confidence": evidence_confidence,
        "confidence_level": confidence_level
    }
