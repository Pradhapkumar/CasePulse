import re
from .legal_nlp_service import clean_legal_text, extract_important_sentences
from .entity_extraction_service import extract_legal_entities
from .direction_classifier import classify_direction
from .highlight_service import get_source_snippets
from .confidence_service import calculate_ai_confidence
from .legal_section_service import extract_legal_sections

def detect_case_type(text: str) -> str:
    text_lower = text.lower()
    if any(k in text_lower for k in ["criminal petition", "criminal appeal", "fir", "accused", "offence", "ipc", "cr.p.c"]):
        return "Criminal"
    if any(k in text_lower for k in ["civil appeal", "civil suit", "plaintiff", "defendant", "property dispute", "specific performance"]):
        return "Civil"
    if any(k in text_lower for k in ["writ petition", "w.p.", "article 226"]):
        return "Writ"
    if "appeal" in text_lower:
        return "Appeal"
    return "General / Manual Verification"

def detect_judgment_date(text: str) -> str:
    # Look for "Date of Judgment", "Judgment Date", etc.
    patterns = [
        r"date of judgment[:\s]+(\d{1,2}[\/\-\s]\w+[\/\-\s]\d{4})",
        r"judgment date[:\s]+(\d{1,2}[\/\-\s]\w+[\/\-\s]\d{4})",
        r"dated this the (\d{1,2}[th|st|rd|nd]* day of \w+, \d{4})",
        r"(\d{1,2}[\/\-\d]{1,2}[\/\-\d]{2,4})"
    ]
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return "Not clearly detected"

def detect_hearings_count(text: str) -> str:
    keywords = ["hearing", "listed on", "next hearing", "heard on", "date of hearing"]
    count = 0
    text_lower = text.lower()
    for k in keywords:
        count += len(re.findall(re.escape(k), text_lower))
    
    if count == 0:
        return "Not clearly mentioned"
    return f"{count} hearings detected from document references"

def extract_case_details(text: str) -> dict:
    cleaned = clean_legal_text(text)
    
    # 1. Entity Extraction
    entities = extract_legal_entities(cleaned)
    
    # 2. NLP Sentences & Directions
    important_sentences = extract_important_sentences(cleaned)
    
    detected_directions = []
    best_score = -1
    best_direction = None
    
    for s in important_sentences:
        cls_dir = classify_direction(s)
        detected_directions.append(cls_dir)
        if cls_dir["score"] > best_score:
            best_score = cls_dir["score"]
            best_direction = cls_dir
            
    # Combine keywords for snippet highlights
    all_matched_keywords = []
    for d in detected_directions:
        all_matched_keywords.extend(d.get("matched_keywords", []))
    all_matched_keywords = list(set(all_matched_keywords))
    
    if not all_matched_keywords:
        all_matched_keywords = ["directed", "shall", "comply", "submit report"]
        
    snippets = get_source_snippets(cleaned, all_matched_keywords)
    source_snippets_text = " || ".join(snippets)
    
    # New Extractions
    case_type = detect_case_type(cleaned)
    judgment_date = detect_judgment_date(cleaned)
    hearings_count = detect_hearings_count(cleaned)
    legal_sections = extract_legal_sections(cleaned)
    
    # Generate mock classified_action based on best_direction to get confidence
    classified_action_mock = {"classification_score": best_direction["score"] if best_direction else 40}
    
    confidence_data = calculate_ai_confidence(entities, classified_action_mock, snippets)
    
    # Prepare JSON structure returning old API fields + new AI fields
    petitioner = entities.get("petitioner")
    respondent = entities.get("respondent")
    
    key_directions = " ".join([d["sentence"] for d in detected_directions]) if detected_directions else None
    
    extracted = {
        "case_number": entities.get("case_number"),
        "court_name": entities.get("court_name"),
        "date_of_order": entities.get("date_of_order"),
        "petitioner": petitioner,
        "respondent": respondent,
        "parties_involved": f"{petitioner} vs {respondent}" if petitioner and respondent else None,
        "key_directions": key_directions,
        "timelines": entities.get("timeline"),
        "responsible_department": entities.get("responsible_department"),
        "important_keywords": ", ".join(all_matched_keywords) if all_matched_keywords else None,
        "source_snippets": source_snippets_text,
        "confidence_score": confidence_data.get("overall_confidence", 0),
        "confidence_breakdown": confidence_data,
        "detected_directions": detected_directions,
        # New fields
        "case_type": case_type,
        "judgment_date": judgment_date,
        "hearings_count": hearings_count,
        "legal_sections": legal_sections
    }
    
    return extracted
