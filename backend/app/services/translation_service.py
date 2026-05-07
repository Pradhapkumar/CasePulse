# Offline translation dictionary for legal terms
LEGAL_DICTIONARY = {
    "ta": {
        "required action": "தேவையான நடவடிக்கை",
        "reason": "காரணம்",
        "source text": "ஆதார உரை",
        "key directions": "முக்கிய திசைகள்",
        "department": "துறை",
        "case number": "வழக்கு எண்",
        "court name": "நீதிமன்றத்தின் பெயர்",
        "petitioner": "மனுதாரர்",
        "respondent": "எதிர்மனுதாரர்",
        "deadline": "காலக்கெடு",
        "priority": "முன்னுரிமை",
        "status": "நிலை",
        "action plan": "நடவடிக்கை திட்டம்",
        "verified": "சரிபார்க்கப்பட்டது",
        "pending": "நிலுவையில் உள்ளது",
        "writ": "ரிட்",
        "civil": "சிவில்",
        "criminal": "குற்றவியல்",
        "appeal": "மேல்முறையீடு",
        "high": "அதிகம்",
        "medium": "நடுத்தரம்",
        "low": "குறைவு",
    },
    "hi": {
        "required action": "आवश्यक कार्रवाई",
        "reason": "कारण",
        "source text": "स्रोत पाठ",
        "key directions": "मुख्य निर्देश",
        "department": "विभाग",
        "case number": "मामला संख्या",
        "court name": "न्यायालय का नाम",
        "petitioner": "याचिकाकर्ता",
        "respondent": "प्रतिवादी",
        "deadline": "समय सीमा",
        "priority": "प्राथमिकता",
        "status": "स्थिति",
        "action plan": "कार्य योजना",
        "verified": "सत्यापित",
        "pending": "लंबित",
        "writ": "रिट",
        "civil": "सिविल",
        "criminal": "आपराधिक",
        "appeal": "अपील",
        "high": "उच्च",
        "medium": "मध्यम",
        "low": "कम",
    },
    "kn": {
        "required action": "ಅಗತ್ಯ ಕ್ರಮ",
        "reason": "ಕಾರಣ",
        "source text": "ಮೂಲ ಪಠ್ಯ",
        "key directions": "ಪ್ರಮುಖ ನಿರ್ದೇಶನಗಳು",
        "department": "ಇಲಾಖೆ",
        "case number": "ಪ್ರಕರಣದ ಸಂಖ್ಯೆ",
        "court name": "ನ್ಯಾಯಾಲಯದ ಹೆಸರು",
        "petitioner": "ಅರ್ಜಿದಾರರು",
        "respondent": "ಪ್ರತಿಕ್ರಿಯೆ ನೀಡುವವರು",
        "deadline": "ಗಡುವು",
        "priority": "ಆದ್ಯತೆ",
        "status": "ಸ್ಥಿತಿ",
        "action plan": "ಕ್ರಿಯಾ ಯೋಜನೆ",
        "verified": "ಪರಿಶೀಲಿಸಲಾಗಿದೆ",
        "pending": "ಬಾಕಿ ಇದೆ",
        "writ": "ರಿಟ್",
        "civil": "ಸಿವಿಲ್",
        "criminal": "ಅಪರಾಧ",
        "appeal": "ಮೇಲ್ಮನವಿ",
        "high": "ಹೆಚ್ಚು",
        "medium": "ಮಧ್ಯಮ",
        "low": "ಕಡಿಮೆ",
    }
}

def translate_text(text: str, target_language: str) -> str:
    if not text:
        return ""
        
    if target_language == "en":
        return text

    # Check for exact matches in the dictionary (case-insensitive)
    lang_dict = LEGAL_DICTIONARY.get(target_language, {})
    if text.lower() in lang_dict:
        return lang_dict[text.lower()]

    # If no exact match, return placeholder for demo
    placeholders = {
        "ta": "மொழிபெயர்ப்பு",
        "hi": "अनुवाद",
        "kn": "ಅನುವಾದ",
        "te": "అనువాదం",
        "ml": "വിവർത്തനം",
        "mr": "भाषांतर",
        "gu": "અનુવાદ",
        "bn": "অনুবাদ",
        "pa": "ਅਨੁਵਾਦ",
        "ur": "ترجمہ",
        "or": "ଅନୁବାଦ"
    }
    
    placeholder = placeholders.get(target_language, "Translated")
    return f"[{placeholder}] {text}"
