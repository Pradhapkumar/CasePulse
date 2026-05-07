import re

def clean_legal_text(text: str) -> str:
    if not text:
        return ""
    # Remove extra spaces
    cleaned = re.sub(r'[ \t]+', ' ', text)
    # Normalize line breaks
    cleaned = re.sub(r'[\r\n]+', '\n', cleaned)
    # Remove some repeating headers/footers roughly (optional, keep it simple)
    # Just basic cleanup
    return cleaned.strip()

def split_into_sentences(text: str) -> list[str]:
    if not text:
        return []
    # Split judgment text into sentences using ., newline, and semicolon
    raw_sentences = re.split(r'[.\n;]+', text)
    # Avoid empty sentences
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 3]
    return sentences

def extract_important_sentences(text: str) -> list[str]:
    sentences = split_into_sentences(text)
    keywords = [
        "directed", "ordered", "shall", "must", "comply", "consider", 
        "dispose", "submit report", "file appeal", "limitation", 
        "within", "petitioner", "respondent", "department"
    ]
    
    important = []
    for s in sentences:
        s_lower = s.lower()
        if any(kw in s_lower for kw in keywords):
            important.append(s)
            
    # Return max 10 important sentences
    return important[:10]
