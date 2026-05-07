def get_source_snippets(text: str, keywords: list) -> list:
    text_lower = text.lower()
    snippets = []
    
    for kw in keywords:
        idx = text_lower.find(kw.lower())
        if idx != -1:
            start = max(0, idx - 50)
            end = min(len(text), idx + 250)
            snippet = text[start:end].replace('\n', ' ').strip()
            snippets.append(snippet)
            if len(snippets) >= 3:
                break
                
    if not snippets:
        snippets.append(text[:300].replace('\n', ' ').strip())
        
    return snippets
