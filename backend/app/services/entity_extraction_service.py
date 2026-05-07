import re
from .department_mapper import map_department
from .deadline_service import detect_deadline

def extract_legal_entities(text: str) -> dict:
    case_number = None
    court_name = None
    date_of_order = None
    petitioner = "Petitioner not clearly detected"
    respondent = "Respondent not clearly detected"

    # Case number
    case_patterns = [
        r'(?:W\.P\.|WP|Case|Civil Appeal|Criminal Petition)\s*No\.?\s*\d+/\d{4}',
        r'[A-Z\.]+\s*No\.?\s*\d+/\d{4}'
    ]
    for pattern in case_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            case_number = match.group(0)
            break
            
    # Court name
    court_patterns = [
        r'High Court of Karnataka',
        r'Supreme Court of India',
        r'District Court',
        r'High Court'
    ]
    for pattern in court_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            court_name = pattern
            break

    # Date of order
    date_patterns = [
        r'\d{1,2}/\d{1,2}/\d{4}',
        r'\d{1,2}-\d{1,2}-\d{4}',
        r'\d{1,2}\s+[A-Za-z]+\s+\d{4}',
        r'[A-Za-z]+\s+\d{1,2},\s+\d{4}'
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_of_order = match.group(0)
            break

    # Petitioner
    pet_patterns = [r'Petitioner:\s*([^\n]+)', r'Petitioner\s*-\s*([^\n]+)', r'BETWEEN:\s*([^\n]+)']
    for pattern in pet_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            petitioner = match.group(1).strip()
            break
            
    # Respondent
    res_patterns = [r'Respondent:\s*([^\n]+)', r'Respondent\s*-\s*([^\n]+)', r'AND:\s*([^\n]+)']
    for pattern in res_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            respondent = match.group(1).strip()
            break

    # Department and timeline
    responsible_department = map_department(text)
    timeline = detect_deadline(text)

    return {
        "case_number": case_number,
        "court_name": court_name,
        "date_of_order": date_of_order,
        "petitioner": petitioner,
        "respondent": respondent,
        "responsible_department": responsible_department,
        "timeline": timeline
    }
