import fitz

def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        
        if not text.strip():
            return "Text extraction failed or scanned PDF detected. Manual review required."
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}")
        return "Text extraction failed or scanned PDF detected. Manual review required."
