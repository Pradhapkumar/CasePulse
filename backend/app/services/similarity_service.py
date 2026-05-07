def text_similarity(text1: str, text2: str) -> int:
    if not text1 or not text2:
        return 0
        
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    
    words1 = set(w for w in text1.lower().split() if w not in stopwords and len(w) > 2)
    words2 = set(w for w in text2.lower().split() if w not in stopwords and len(w) > 2)
    
    if not words1 or not words2:
        return 0
        
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    similarity = (len(intersection) / len(union)) * 100
    return int(similarity)

def find_similar_cases(current_text: str, existing_cases: list) -> list:
    similar_cases = []
    for case in existing_cases:
        sim_score = text_similarity(current_text, case.get("text", ""))
        if sim_score >= 70:
            similar_cases.append({
                "case_id": case.get("case_id"),
                "similarity_score": sim_score
            })
    return similar_cases
