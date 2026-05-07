import re

# Simple dictionary for common criminal sections
SECTION_TITLES = {
    "IPC": {
        "302": "Murder",
        "304B": "Dowry death",
        "307": "Attempt to murder",
        "323": "Voluntarily causing hurt",
        "354": "Assault or criminal force to woman with intent to outrage modesty",
        "376": "Rape",
        "379": "Theft",
        "406": "Criminal breach of trust",
        "409": "Criminal breach of trust by public servant",
        "420": "Cheating and dishonestly inducing delivery of property",
        "467": "Forgery of valuable security",
        "468": "Forgery for purpose of cheating",
        "471": "Using forged document as genuine",
        "498A": "Cruelty by husband or relatives",
        "506": "Criminal intimidation",
        "120B": "Criminal conspiracy",
        "34": "Common intention"
    },
    "CrPC": {
        "125": "Maintenance",
        "156(3)": "Magistrate order for investigation",
        "439": "Bail",
        "482": "High Court inherent powers"
    },
    "NI Act": {
        "138": "Dishonour of cheque"
    },
    "IT Act": {
        "66": "Computer-related offences",
        "67": "Publishing or transmitting obscene material"
    }
}

def detect_act_name(sentence: str) -> str:
    sentence = sentence.upper()
    if any(x in sentence for x in ["IPC", "INDIAN PENAL CODE"]):
        return "IPC"
    if any(x in sentence for x in ["CRPC", "CODE OF CRIMINAL PROCEDURE"]):
        return "CrPC"
    if any(x in sentence for x in ["BNS", "BHARATIYA NYAYA SANHITA"]):
        return "BNS"
    if any(x in sentence for x in ["BNSS", "BHARATIYA NAGARIK SURAKSHA SANHITA"]):
        return "BNSS"
    if "EVIDENCE ACT" in sentence:
        return "Evidence Act"
    if "NEGOTIABLE INSTRUMENTS ACT" in sentence:
        return "NI Act"
    if "PREVENTION OF CORRUPTION ACT" in sentence:
        return "Prevention of Corruption Act"
    if "DOWRY PROHIBITION ACT" in sentence:
        return "Dowry Prohibition Act"
    if any(x in sentence for x in ["IT ACT", "INFORMATION TECHNOLOGY ACT"]):
        return "IT Act"
    if "MOTOR VEHICLES ACT" in sentence:
        return "Motor Vehicles Act"
    if "NDPS ACT" in sentence:
        return "NDPS Act"
    if "POCSO ACT" in sentence:
        return "POCSO Act"
    if "ARMS ACT" in sentence:
        return "Arms Act"
    
    return "Act not clearly detected"

def get_section_title(section_number: str, act_name: str) -> str:
    # Normalize act name for dictionary lookup
    lookup_act = act_name
    if act_name == "Indian Penal Code": lookup_act = "IPC"
    if act_name == "Code of Criminal Procedure": lookup_act = "CrPC"
    if "Negotiable Instruments" in act_name: lookup_act = "NI Act"
    if "Information Technology" in act_name: lookup_act = "IT Act"

    return SECTION_TITLES.get(lookup_act, {}).get(section_number, "Section title not available in prototype")

def extract_punishment(text: str) -> dict:
    punishment_patterns = [
        r"(sentenced to imprisonment for\s+[^.]*)",
        r"(rigorous imprisonment for\s+[^.]*)",
        r"(simple imprisonment for\s+[^.]*)",
        r"(imprisonment for a period of\s+[^.]*)",
        r"(sentenced to undergo\s+[^.]*)",
        r"(fine of Rs\.\s*\d+[^.]*)",
        r"(fine of ₹\s*\d+[^.]*)",
        r"(penalty of\s+[^.]*)",
        r"(life imprisonment)",
        r"(death sentence)",
        r"(acquitted)"
    ]
    
    found_punishments = []
    for pattern in punishment_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_punishments.extend(matches)
            
    if not found_punishments:
        return {
            "punishment": "Punishment not explicitly mentioned in judgment text",
            "explicit": False
        }
    
    return {
        "punishment": "; ".join(found_punishments),
        "explicit": True
    }

def extract_legal_sections(text: str) -> list[dict]:
    # Broad patterns to find sentences containing sections
    section_patterns = [
        r"(?:Section|Sections|Sec\.|u/s|under Section)\s+([0-9A-Z,\s&and]+)\s+(?:of|in)?\s*([A-Za-z\s]+Act|IPC|CrPC|BNS|BNSS|Indian Penal Code|Code of Criminal Procedure|Bharatiya Nyaya Sanhita|Bharatiya Nagarik Suraksha Sanhita)"
    ]
    
    results = []
    
    # Split text into sentences for context
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        for pattern in section_patterns:
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            for match in matches:
                section_raw = match.group(1).strip()
                # Handle comma separated sections like 120B, 420
                section_list = [s.strip() for s in re.split(r',|&|\band\b', section_raw) if s.strip()]
                
                detected_act = detect_act_name(sentence)
                if detected_act == "Act not clearly detected":
                    # Try to detect from the second group if sentence failed
                    detected_act = detect_act_name(match.group(2))

                punishment_info = extract_punishment(sentence)

                for sec_num in section_list:
                    results.append({
                        "section_number": sec_num,
                        "act_name": detected_act,
                        "section_title": get_section_title(sec_num, detected_act),
                        "punishment": punishment_info["punishment"],
                        "punishment_explicit": punishment_info["explicit"],
                        "source_evidence": sentence,
                        "confidence_score": 0.85 # Prototype fixed score
                    })
    
    # Remove duplicates
    unique_results = []
    seen = set()
    for res in results:
        key = f"{res['section_number']}-{res['act_name']}"
        if key not in seen:
            unique_results.append(res)
            seen.add(key)
            
    return unique_results
