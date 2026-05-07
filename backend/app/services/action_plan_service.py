import json
from .legal_nlp_service import extract_important_sentences, clean_legal_text
from .entity_extraction_service import extract_legal_entities
from .action_classifier import classify_action_plan
from .risk_service import calculate_compliance_risk

def generate_action_plan(extracted_data: dict, raw_text: str) -> dict:
    cleaned = clean_legal_text(raw_text)
    important_sentences = extract_important_sentences(cleaned)
    entities = extract_legal_entities(cleaned)
    
    # Generate action plan classification
    action_plan_data = classify_action_plan(cleaned, important_sentences, entities)
    
    confidence_score = extracted_data.get("confidence_score")
    if confidence_score is None:
        confidence_score = 0
    elif isinstance(confidence_score, dict):
        confidence_score = confidence_score.get("overall_confidence", 0)
        
    risk_data = calculate_compliance_risk(
        action_plan_data["action_type"],
        action_plan_data["deadline"],
        confidence_score,
        action_plan_data["source_text"]
    )
    
    return {
        "action_type": action_plan_data["action_type"],
        "required_action": action_plan_data["required_action"],
        "responsible_department": action_plan_data["responsible_department"],
        "deadline": action_plan_data["deadline"],
        "priority": action_plan_data["priority"],
        "risk_level": risk_data["risk_level"],
        "risk_score": risk_data["risk_score"],
        "risk_factors": json.dumps(risk_data["risk_factors"]),
        "reason": action_plan_data["reason"],
        "source_text": action_plan_data["source_text"],
        "confidence_score": confidence_score
    }
