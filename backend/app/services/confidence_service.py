"""
Confidence Score Service
Computes a confidence score (0.0 – 1.0) for AI-extracted case data.
Score is based on how many key fields were successfully extracted.
"""

from typing import Dict, Any, List


# Weight assigned to each field (total = 1.0)
FIELD_WEIGHTS: Dict[str, float] = {
    "case_number":   0.20,
    "court_name":    0.10,
    "parties":       0.15,
    "directions":    0.20,
    "department":    0.10,
    "deadlines":     0.15,
    "risk_level":    0.10,
}


class ConfidenceService:
    """Computes a confidence score for extracted case data."""

    def compute(self, extracted_data: Dict[str, Any]) -> float:
        """
        Compute overall confidence score for the extracted data.

        Args:
            extracted_data: Dictionary produced by extraction_service.

        Returns:
            Float between 0.0 and 1.0 representing extraction confidence.
        """
        score = 0.0

        for field, weight in FIELD_WEIGHTS.items():
            value = extracted_data.get(field)
            if self._is_present(value):
                score += weight

        return round(min(score, 1.0), 2)

    def get_label(self, score: float) -> str:
        """
        Convert numeric score to a human-readable confidence label.

        Args:
            score: Float 0.0 – 1.0

        Returns:
            'High', 'Medium', or 'Low'
        """
        if score >= 0.75:
            return "High"
        elif score >= 0.45:
            return "Medium"
        else:
            return "Low"

    def get_report(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return a full confidence report with per-field breakdown.

        Args:
            extracted_data: Dictionary produced by extraction_service.

        Returns:
            Dict with overall score, label, and field-level results.
        """
        breakdown: List[Dict[str, Any]] = []

        for field, weight in FIELD_WEIGHTS.items():
            value = extracted_data.get(field)
            present = self._is_present(value)
            breakdown.append({
                "field":   field,
                "present": present,
                "weight":  weight,
                "earned":  weight if present else 0.0,
            })

        overall = sum(item["earned"] for item in breakdown)
        overall = round(min(overall, 1.0), 2)

        return {
            "score":     overall,
            "label":     self.get_label(overall),
            "breakdown": breakdown,
        }

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _is_present(value: Any) -> bool:
        """Return True if a field has a meaningful, non-empty value."""
        if value is None:
            return False
        if isinstance(value, str):
            return len(value.strip()) > 0
        if isinstance(value, (list, dict)):
            return len(value) > 0
        return True
