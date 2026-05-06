"""
Department Mapper Service
Detects the responsible government department from judgment text.
Supports: Revenue, Police, Education, Health, PWD, Municipal, Forest,
          Agriculture, Labour, Social Welfare, and more.
"""

import re
from typing import List, Dict, Optional


# ---------------------------------------------------------------------------
# Keyword → Department mapping
# Order matters: more specific entries first.
# ---------------------------------------------------------------------------
DEPARTMENT_KEYWORDS: Dict[str, List[str]] = {
    "Revenue Department": [
        "revenue", "tahsildar", "sub-registrar", "land acquisition",
        "patta", "chitta", "encumbrance", "collector", "district collector",
        "taluk", "land record", "survey number",
    ],
    "Police Department": [
        "police", "inspector", "superintendent of police", "s.p.",
        "d.s.p.", "fir", "first information report", "station house officer",
        "custody", "arrested", "detention",
    ],
    "Education Department": [
        "education", "school", "college", "university", "headmaster",
        "teacher", "student", "academic", "admission", "scholarship",
        "directorate of school education", "higher education",
    ],
    "Health Department": [
        "health", "hospital", "doctor", "medical officer", "physician",
        "nurse", "patient", "treatment", "drug", "pharmacy",
        "directorate of health", "public health",
    ],
    "Public Works Department (PWD)": [
        "public works", "pwd", "road", "bridge", "construction",
        "contractor", "tender", "infrastructure",
    ],
    "Municipal Administration": [
        "municipality", "municipal", "corporation", "town panchayat",
        "urban local body", "town planning", "building permit",
        "property tax", "drainage",
    ],
    "Forest Department": [
        "forest", "wildlife", "timber", "encroachment", "panchayat forest",
        "tree cutting", "forest officer", "sanctuary",
    ],
    "Agriculture Department": [
        "agriculture", "farmer", "crop", "irrigation", "seed",
        "fertilizer", "horticulture", "agri", "kisan",
    ],
    "Labour Department": [
        "labour", "worker", "employee", "factory", "workmen",
        "industrial dispute", "provident fund", "esic", "wages",
        "minimum wages", "gratuity",
    ],
    "Social Welfare Department": [
        "social welfare", "sc/st", "scheduled caste", "scheduled tribe",
        "backward class", "welfare scheme", "pension", "disability",
        "adi dravidar",
    ],
    "Electricity Board": [
        "electricity", "power", "tangedco", "tneb", "meter",
        "power supply", "tariff", "transformer",
    ],
    "Judiciary / Court Administration": [
        "court", "tribunal", "judge", "magistrate", "high court",
        "supreme court", "sessions court", "district court",
    ],
}


class DepartmentMapper:
    """Detects the responsible department from case text."""

    def detect(self, text: str) -> Optional[str]:
        """
        Return the best-matching department name, or None.

        Args:
            text: Full extracted text from the judgment.

        Returns:
            Department name string or None if no match found.
        """
        text_lower = text.lower()
        scores: Dict[str, int] = {}

        for dept, keywords in DEPARTMENT_KEYWORDS.items():
            count = sum(
                len(re.findall(r'\b' + re.escape(kw) + r'\b', text_lower))
                for kw in keywords
            )
            if count > 0:
                scores[dept] = count

        if not scores:
            return None

        # Return the department with the highest keyword hit count
        return max(scores, key=lambda d: scores[d])

    def detect_all(self, text: str) -> List[str]:
        """
        Return all matching departments (in descending match order).

        Useful when a case involves multiple departments.

        Args:
            text: Full extracted text from the judgment.

        Returns:
            List of department names sorted by relevance.
        """
        text_lower = text.lower()
        scores: Dict[str, int] = {}

        for dept, keywords in DEPARTMENT_KEYWORDS.items():
            count = sum(
                len(re.findall(r'\b' + re.escape(kw) + r'\b', text_lower))
                for kw in keywords
            )
            if count > 0:
                scores[dept] = count

        return sorted(scores.keys(), key=lambda d: scores[d], reverse=True)

    def get_all_departments(self) -> List[str]:
        """Return the full list of supported department names."""
        return list(DEPARTMENT_KEYWORDS.keys())
