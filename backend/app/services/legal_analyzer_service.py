import re

LEGAL_KNOWLEDGE_BASE = {
    "IPC": {
        "420": {
            "meaning": "Cheating and dishonestly inducing delivery of property. It involves deceiving someone to deliver property or to make, alter, or destroy a valuable security.",
            "legal_steps": ["Register an FIR for cheating.", "Establish evidence of inducement and deception.", "Show loss of property or valuable security."],
            "action_required": "Identify the specific misrepresentation made by the accused and collect bank statements or receipts as proof of transaction."
        },
        "468": {
            "meaning": "Forgery for the purpose of cheating. Using forged documents to commit a fraud.",
            "legal_steps": ["Collect original and suspected forged documents.", "Request forensic examination of signatures.", "Connect forgery to a specific act of cheating."],
            "action_required": "Secure the primary document and maintain a chain of custody for forensic validation."
        },
        "471": {
            "meaning": "Using as genuine a forged document. Passing off a fake document as real despite knowing it's forged.",
            "legal_steps": ["Prove the document is forged.", "Prove the accused knew it was forged.", "Prove it was used in a transaction."],
            "action_required": "Document the context where the document was submitted (e.g., to a bank or government office)."
        },
        "120B": {
            "meaning": "Criminal conspiracy. An agreement between two or more persons to commit an illegal act.",
            "legal_steps": ["Establish meeting of minds between accused.", "Trace call records or digital footprints.", "Find evidence of an overt act in furtherance of the conspiracy."],
            "action_required": "Analyze communication logs and witness statements to prove a pre-planned agreement."
        },
        "406": {
            "meaning": "Punishment for criminal breach of trust. Dishonest misappropriation of property entrusted to the person.",
            "legal_steps": ["Establish that property was entrusted.", "Prove dishonest misappropriation.", "Demonstrate violation of any legal contract."],
            "action_required": "Collect receipts and agreements showing the initial entrustment of property."
        }
    },
    "CrPC": {
        "439": {
            "meaning": "Special powers of High Court or Court of Session regarding bail. Allows higher courts to grant bail even in non-bailable offences.",
            "legal_steps": ["File a regular bail application.", "Argue on merits and change in circumstances.", "Demonstrate that the accused is not a flight risk."],
            "action_required": "Draft a strong bail petition highlighting civil liberties and lack of prima facie evidence."
        },
        "482": {
            "meaning": "Inherent powers of High Court. Allows the High Court to pass orders to prevent abuse of the process of any court or to secure the ends of justice.",
            "legal_steps": ["File a petition to quash FIR or proceedings.", "Show that the case is purely civil or lacks criminal ingredients.", "Cite abuse of legal process."],
            "action_required": "Prepare a comprehensive petition demonstrating how the lower court's proceedings are legally unsustainable."
        },
        "313": {
            "meaning": "Power to examine the accused. The court questions the accused to explain any circumstances appearing in the evidence against him.",
            "legal_steps": ["Accused must respond personally without taking oath.", "Explain incriminating evidence.", "Officer must ensure no pressure is applied."],
            "action_required": "Judicial officer must prepare specific questions based on the prosecution's evidence."
        }
    },
    "Evidence Act": {
        "65B": {
            "meaning": "Admissibility of electronic records. Requires a special certificate to prove the authenticity of digital evidence like emails, WhatsApp, or CCTV.",
            "legal_steps": ["Obtain a 65B Certificate from the system administrator.", "Ensure the computer used was in proper working order.", "Verify hash values of files."],
            "action_required": "Attach the mandatory 65B certificate along with the electronic evidence during filing."
        },
        "27": {
            "meaning": "How much of information received from accused may be proved. Only the portion that leads to the discovery of a specific fact/object is admissible.",
            "legal_steps": ["Recovery of an object based on accused statement.", "Statement must be made in custody.", "Record the exact words leading to discovery."],
            "action_required": "Draft a recovery memo (Panchnama) specifying the exact location and object discovered."
        }
    },
    "Constitution": {
        "226": {
            "meaning": "Power of High Courts to issue certain writs (Habeas Corpus, Mandamus, etc.) for enforcement of fundamental rights and for any other purpose.",
            "legal_steps": ["File a Writ Petition in the High Court.", "Demonstrate violation of Fundamental Rights.", "Show lack of alternative remedy."],
            "action_required": "Specify the exact Fundamental Right infringed and the state action responsible."
        },
        "227": {
            "meaning": "Power of superintendence over all courts by the High Court. High Court can monitor lower courts and tribunals.",
            "legal_steps": ["File a petition against a lower court's order.", "Show jurisdictional error or manifest injustice.", "Argue on supervisory grounds."],
            "action_required": "Highlight procedural irregularities or errors of law in the lower court's judgment."
        },
        "21": {
            "meaning": "Protection of Life and Personal Liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law.",
            "legal_steps": ["Argue for fair trial and speedy justice.", "Challenge arbitrary detention.", "Link to right to dignity and privacy."],
            "action_required": "Ensure all legal procedures are followed strictly to prevent encroachment on personal freedom."
        }
    }
}

def analyze_legal_query(query: str) -> dict:
    query = query.upper()
    
    # Simple regex to catch numbers
    num_match = re.search(r'(\d+[A-Z]?)', query)
    num = num_match.group(1) if num_match else ""
    
    # Detect category
    category = "IPC" # Default
    if "CRPC" in query or "CR.P.C" in query: category = "CrPC"
    elif "EVIDENCE" in query: category = "Evidence Act"
    elif "CONSTITUTION" in query or "ARTICLE" in query: category = "Constitution"
    
    # Try to find in DB
    cat_db = LEGAL_KNOWLEDGE_BASE.get(category, {})
    
    # If not found directly, try IPC for common numbers if they just typed "420"
    if num and num not in cat_db and category == "IPC":
        # Fallback check
        pass

    result = cat_db.get(num)
    
    if result:
        return {
            "found": True,
            "section": f"{category} Section/Article {num}",
            "meaning": result["meaning"],
            "legalSteps": result["legal_steps"],
            "actionRequired": result["action_required"]
        }
    
    return {
        "found": False,
        "message": f"I couldn't find a specific detailed explanation for '{query}' in my current knowledge base, but I can still extract it from judgments."
    }
