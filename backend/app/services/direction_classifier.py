import re

def classify_direction(sentence: str) -> dict:
    sentence_lower = sentence.lower()
    
    classes = {
        "COMPLIANCE_DIRECTION": ["directed to", "shall", "comply", "pass appropriate orders", "consider the application", "dispose of"],
        "REPORT_SUBMISSION": ["submit report", "compliance report", "status report"],
        "APPEAL_REVIEW": ["appeal", "limitation", "review petition", "writ appeal"],
        "NOTICE_OR_HEARING": ["next hearing", "notice", "appear before", "list the matter"]
    }
    
    best_label = "MANUAL_REVIEW"
    best_score = 0
    matched_kws = []
    
    for label, keywords in classes.items():
        score = 40
        matched = [kw for kw in keywords if kw in sentence_lower]
        if matched:
            score += 20 * len(matched)
            
            # Simple checks for timeline and department in sentence
            if any(t in sentence_lower for t in ["within", "days", "weeks", "months"]):
                score += 20
            if any(d in sentence_lower for d in ["department", "authority", "commissioner"]):
                score += 10
                
            score = min(score, 100)
            
            if score > best_score:
                best_score = score
                best_label = label
                matched_kws = matched

    if best_label == "MANUAL_REVIEW":
        best_score = 40 # Base score for manual review

    return {
        "label": best_label,
        "matched_keywords": matched_kws,
        "score": best_score,
        "sentence": sentence
    }
