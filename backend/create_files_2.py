import os

base_dir = r'c:\Users\prdha\OneDrive\Desktop\CAsePulse_Bangalore\backend'
files = {}

files['app/services/pdf_service.py'] = """import fitz

def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\\n"
        doc.close()
        
        if not text.strip():
            return "Text extraction failed or scanned PDF detected. Manual review required."
        return text
    except Exception as e:
        return "Text extraction failed or scanned PDF detected. Manual review required."
"""

files['app/utils/text_cleaner.py'] = """import re

def clean_text(text: str) -> str:
    text = re.sub(r'\\s+', ' ', text)
    text = text.replace('\\r\\n', '\\n')
    return text.strip()
"""

files['app/utils/regex_patterns.py'] = """import re

CASE_NUMBER_PATTERN = re.compile(r'(?:W\\.P\\.|WP|Case|Civil Appeal|Criminal Petition)\\s*(?:No\\.)?\\s*\\d+/\\d{4}', re.IGNORECASE)
DATE_PATTERN = re.compile(r'\\b(\\d{1,2}[/-]\\d{1,2}[/-]\\d{4}|\\d{1,2}\\s+[A-Za-z]+\\s+\\d{4})\\b')
"""

files['app/services/department_mapper.py'] = """def map_department(text: str) -> str:
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
"""

files['app/services/deadline_service.py'] = """def detect_deadline(text: str) -> str:
    text_lower = text.lower()
    deadlines = [
        "within 30 days", "within 60 days", "within four weeks", "within two months",
        "30 days", "60 days", "4 weeks", "2 months"
    ]
    for d in deadlines:
        if d in text_lower:
            return d
    return "No explicit deadline detected"
"""

files['app/services/highlight_service.py'] = """def get_source_snippets(text: str, keywords: list) -> list:
    text_lower = text.lower()
    snippets = []
    
    for kw in keywords:
        idx = text_lower.find(kw.lower())
        if idx != -1:
            start = max(0, idx - 50)
            end = min(len(text), idx + 250)
            snippet = text[start:end].replace('\\n', ' ').strip()
            snippets.append(snippet)
            if len(snippets) >= 3:
                break
                
    if not snippets:
        snippets.append(text[:300].replace('\\n', ' ').strip())
        
    return snippets
"""

files['app/services/confidence_service.py'] = """def calculate_confidence(extracted: dict) -> int:
    score = 0
    if extracted.get("case_number"): score += 20
    if extracted.get("date_of_order"): score += 20
    if extracted.get("court_name") and "not clearly detected" not in extracted.get("court_name", ""): score += 20
    if extracted.get("key_directions"): score += 20
    
    t = extracted.get("timelines", "")
    d = extracted.get("responsible_department", "")
    if "No explicit deadline" not in t or "requires manual verification" not in d:
        score += 20
        
    return min(100, score)
"""

files['app/services/extraction_service.py'] = """import re
from .department_mapper import map_department
from .deadline_service import detect_deadline
from .highlight_service import get_source_snippets
from .confidence_service import calculate_confidence
from ..utils.regex_patterns import CASE_NUMBER_PATTERN, DATE_PATTERN
from ..utils.text_cleaner import clean_text

def extract_case_details(text: str) -> dict:
    cleaned = clean_text(text)
    
    # Case number
    case_num_match = CASE_NUMBER_PATTERN.search(cleaned)
    case_number = case_num_match.group(0) if case_num_match else None
    
    # Court name
    if "High Court of Karnataka" in cleaned:
        court_name = "High Court of Karnataka"
    elif "High Court" in cleaned:
        court_name = "High Court"
    elif "Supreme Court" in cleaned:
        court_name = "Supreme Court of India"
    else:
        court_name = "Court not clearly detected"
        
    # Date
    date_match = DATE_PATTERN.search(cleaned)
    date_of_order = date_match.group(0) if date_match else None
    
    # Petitioner & Respondent
    petitioner = None
    respondent = None
    pet_match = re.search(r'Petitioner:\\s*([^\\n]+)', cleaned, re.IGNORECASE)
    if pet_match: petitioner = pet_match.group(1).strip()
    res_match = re.search(r'Respondent:\\s*([^\\n]+)', cleaned, re.IGNORECASE)
    if res_match: respondent = res_match.group(1).strip()
    
    # Key directions
    directions = []
    direction_keywords = ["directed to", "ordered to", "shall", "comply", "submit report", "consider", "dispose of", "pass appropriate orders"]
    sentences = re.split(r'(?<=[.!?])\\s+', cleaned)
    for s in sentences:
        if any(kw in s.lower() for kw in direction_keywords):
            directions.append(s)
    key_directions = " ".join(directions) if directions else None
    
    # Timelines
    timelines = detect_deadline(cleaned)
    
    # Responsible Department
    responsible_department = map_department(cleaned)
    
    # Important Keywords
    keywords_list = ["directed", "compliance", "appeal", "limitation", "report", "deadline", "department"]
    found_kws = [kw for kw in keywords_list if kw in cleaned.lower()]
    important_keywords = ", ".join(found_kws) if found_kws else None
    
    # Source Snippets
    snippets = get_source_snippets(cleaned, found_kws)
    source_snippets_text = " || ".join(snippets)
    
    extracted = {
        "case_number": case_number,
        "court_name": court_name,
        "date_of_order": date_of_order,
        "petitioner": petitioner,
        "respondent": respondent,
        "parties_involved": f"{petitioner} vs {respondent}" if petitioner and respondent else None,
        "key_directions": key_directions,
        "timelines": timelines,
        "responsible_department": responsible_department,
        "important_keywords": important_keywords,
        "source_snippets": source_snippets_text
    }
    
    extracted["confidence_score"] = calculate_confidence(extracted)
    
    return extracted
"""

files['app/services/risk_service.py'] = """def calculate_risk(priority: str, confidence_score: int, deadline: str) -> str:
    if confidence_score < 50:
        return "High"
    if deadline != "No explicit deadline detected" and priority == "High":
        return "High"
    if deadline == "No explicit deadline detected":
        return "Medium"
    return "Low"
"""

files['app/services/action_plan_service.py'] = """from .risk_service import calculate_risk

def generate_action_plan(extracted_data: dict, raw_text: str) -> dict:
    text_lower = raw_text.lower()
    
    if "appeal" in text_lower or "limitation" in text_lower:
        action_type = "Appeal Review"
    elif "submit report" in text_lower:
        action_type = "Report Submission"
    elif any(kw in text_lower for kw in ["directed to", "shall", "comply", "consider", "dispose of", "pass appropriate orders"]):
        action_type = "Compliance"
    else:
        action_type = "Manual Review"
        
    deadline = extracted_data.get("timelines", "No explicit deadline detected")
    dept = extracted_data.get("responsible_department", "Department requires manual verification")
    
    priority = "Medium"
    if deadline != "No explicit deadline detected":
        priority = "High"
    if "appeal" in text_lower or "limitation" in text_lower:
        priority = "High"
        
    risk_level = calculate_risk(priority, extracted_data.get("confidence_score", 0), deadline)
    
    if dept != "Department requires manual verification":
        if deadline != "No explicit deadline detected":
            required_action = f"The {dept} must complete the required action within {deadline}."
        else:
            required_action = f"The {dept} must complete the required action mentioned in the judgment."
    else:
        required_action = "Review the judgment and ensure the responsible department completes the required action."
        
    reason = "Time-bound court direction detected from the judgment source text."
    if "appeal" in text_lower or "limitation" in text_lower:
        reason = "Appeal or limitation-related text detected. Legal review is required."
        
    snippets = extracted_data.get("source_snippets", "").split(" || ")
    source_text = snippets[0] if snippets else ""
    
    return {
        "action_type": action_type,
        "required_action": required_action,
        "responsible_department": dept,
        "deadline": deadline,
        "priority": priority,
        "risk_level": risk_level,
        "reason": reason,
        "source_text": source_text,
        "confidence_score": extracted_data.get("confidence_score", 0)
    }
"""

files['app/services/audit_service.py'] = """from ..models import AuditLog
from sqlalchemy.orm import Session
import datetime

def create_audit_log(db: Session, case_id: int, action: str, performed_by: str, old_value: str = None, new_value: str = None):
    audit = AuditLog(
        case_id=case_id,
        action=action,
        performed_by=performed_by,
        old_value=old_value,
        new_value=new_value,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit
"""

files['app/services/translation_service.py'] = """def translate_text(text: str, target_language: str) -> str:
    if target_language == "ta":
        return f"[Tamil Translation Placeholder] {text}"
    elif target_language == "kn":
        return f"[Kannada Translation Placeholder] {text}"
    elif target_language == "hi":
        return f"[Hindi Translation Placeholder] {text}"
    return text
"""

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
