"""
Deadline Service
Detects deadline expressions from judgment text such as:
  "within 30 days", "4 weeks", "three months", "forthwith", etc.
Returns structured deadline objects with computed due-dates.
"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any


# ---------------------------------------------------------------------------
# Word → number map for written-out numbers
# ---------------------------------------------------------------------------
WORD_NUMBERS: Dict[str, int] = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20,
    "thirty": 30, "forty": 40, "forty-five": 45, "sixty": 60,
    "ninety": 90, "hundred": 100,
}

# ---------------------------------------------------------------------------
# Regex patterns for timeline expressions
# ---------------------------------------------------------------------------
TIMELINE_PATTERNS: List[Dict[str, Any]] = [
    # "within 30 days" / "within 4 weeks" / "within 3 months"
    {
        "pattern": r'\bwithin\s+(\d+|' + '|'.join(WORD_NUMBERS.keys()) + r')\s+(day|days|week|weeks|month|months)\b',
        "type": "relative",
    },
    # "30 days from" / "4 weeks from"
    {
        "pattern": r'\b(\d+|' + '|'.join(WORD_NUMBERS.keys()) + r')\s+(day|days|week|weeks|month|months)\s+from\b',
        "type": "relative",
    },
    # "forthwith" / "immediately"
    {
        "pattern": r'\b(forthwith|immediately|at once|without delay)\b',
        "type": "immediate",
    },
    # "on or before DD/MM/YYYY"
    {
        "pattern": r'\bon or before\s+(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b',
        "type": "absolute",
    },
    # "next hearing" / "next date"
    {
        "pattern": r'\b(next hearing|next date|adjourned to|posted to)\b',
        "type": "next_hearing",
    },
]

# ---------------------------------------------------------------------------
# Unit → days conversion
# ---------------------------------------------------------------------------
UNIT_TO_DAYS: Dict[str, int] = {
    "day": 1,  "days": 1,
    "week": 7, "weeks": 7,
    "month": 30, "months": 30,
}


class DeadlineService:
    """Detects and parses deadline expressions from court judgment text."""

    def extract(self, text: str, reference_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Find all deadline expressions in the text and return structured records.

        Args:
            text           : Extracted judgment text.
            reference_date : Base date for computing due-dates (default: today).

        Returns:
            List of deadline dicts with keys:
                raw_text, type, days, due_date, snippet
        """
        if reference_date is None:
            reference_date = datetime.now()

        text_lower = text.lower()
        results: List[Dict[str, Any]] = []
        seen_spans = set()

        for spec in TIMELINE_PATTERNS:
            for match in re.finditer(spec["pattern"], text_lower, re.IGNORECASE):
                span = match.span()
                # Skip overlapping matches
                if any(s[0] <= span[0] <= s[1] for s in seen_spans):
                    continue
                seen_spans.add(span)

                raw = match.group(0)
                deadline = self._build_deadline(raw, spec["type"], match, reference_date, text, span)
                results.append(deadline)

        return results

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _build_deadline(
        self,
        raw: str,
        dtype: str,
        match: re.Match,
        ref: datetime,
        full_text: str,
        span: tuple,
    ) -> Dict[str, Any]:
        """Construct a structured deadline record from a regex match."""

        days = None
        due_date = None

        if dtype == "immediate":
            days = 0
            due_date = ref.strftime("%Y-%m-%d")

        elif dtype == "relative":
            groups = match.groups()
            qty_str = groups[0].strip().lower()
            unit = groups[1].strip().lower()

            qty = WORD_NUMBERS.get(qty_str) or self._safe_int(qty_str) or 0
            multiplier = UNIT_TO_DAYS.get(unit, 1)
            days = qty * multiplier
            due_date = (ref + timedelta(days=days)).strftime("%Y-%m-%d")

        elif dtype == "absolute":
            raw_date_str = match.group(1)
            parsed = self._parse_date(raw_date_str)
            if parsed:
                due_date = parsed.strftime("%Y-%m-%d")
                days = max((parsed - ref).days, 0)

        elif dtype == "next_hearing":
            # Cannot compute exact date; flag for manual entry
            days = None
            due_date = None

        # Grab surrounding snippet (100 chars each side)
        start = max(span[0] - 100, 0)
        end = min(span[1] + 100, len(full_text))
        snippet = full_text[start:end].strip()

        return {
            "raw_text": raw,
            "type":     dtype,
            "days":     days,
            "due_date": due_date,
            "snippet":  snippet,
        }

    @staticmethod
    def _safe_int(value: str) -> Optional[int]:
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
                    "%d/%m/%y", "%d-%m-%y", "%d.%m.%y"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None
