"""
Risk Assessment Service
-----------------------
Evaluates extracted deadlines and assigns a risk level:

    High   → due_date is within 7 days  (or already overdue)
    Medium → due_date is 8–30 days away
    Low    → due_date is more than 30 days away
    Unknown→ due_date could not be determined (next_hearing type, etc.)

Also produces an overall case-level risk summary.
"""

from datetime import datetime, date
from typing import List, Dict, Any, Optional


# ── Thresholds (days) ───────────────────────────────────────────────────────
HIGH_THRESHOLD   = 7    # ≤ 7 days  → High Risk
MEDIUM_THRESHOLD = 30   # ≤ 30 days → Medium Risk
# > 30 days → Low Risk


class RiskService:
    """Classifies deadline urgency and computes overall case risk level."""

    # ------------------------------------------------------------------ #
    #  Public API
    # ------------------------------------------------------------------ #

    def assess(self, deadlines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess risk for a list of deadline objects returned by DeadlineService.

        Args:
            deadlines: List of deadline dicts with at least 'due_date' and 'raw_text'.

        Returns:
            Dict with:
                overall_risk   : 'High' | 'Medium' | 'Low' | 'Unknown'
                risk_color     : hex colour for UI badge
                flagged_items  : list of high-risk deadline records
                all_items      : full list with individual risk labels
        """
        if not deadlines:
            return self._summary("Unknown", [], [])

        today = date.today()
        all_items: List[Dict[str, Any]] = []
        flagged:   List[Dict[str, Any]] = []

        for dl in deadlines:
            item = self._classify(dl, today)
            all_items.append(item)
            if item["risk_level"] == "High":
                flagged.append(item)

        overall = self._aggregate_risk(all_items)
        return self._summary(overall, flagged, all_items)

    def classify_single(self, deadline: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a single deadline dict.

        Args:
            deadline: One deadline record from DeadlineService.

        Returns:
            Same dict enriched with 'risk_level', 'risk_color', 'days_remaining'.
        """
        return self._classify(deadline, date.today())

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _classify(self, deadline: Dict[str, Any], today: date) -> Dict[str, Any]:
        """Add risk_level, risk_color, and days_remaining to a deadline record."""
        due_date_str: Optional[str] = deadline.get("due_date")
        days: Optional[int] = deadline.get("days")

        # Resolve days_remaining from due_date string or pre-computed days field
        days_remaining = self._days_remaining(due_date_str, days, today)

        risk_level, risk_color = self._level_from_days(days_remaining)

        return {
            **deadline,
            "days_remaining": days_remaining,
            "risk_level":     risk_level,
            "risk_color":     risk_color,
        }

    @staticmethod
    def _days_remaining(
        due_date_str: Optional[str],
        pre_days: Optional[int],
        today: date,
    ) -> Optional[int]:
        """Parse due_date string (YYYY-MM-DD) → days remaining from today."""
        if due_date_str:
            try:
                due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                return (due - today).days
            except ValueError:
                pass
        # Fall back to pre-computed days (might be relative from upload date)
        return pre_days

    @staticmethod
    def _level_from_days(days: Optional[int]):
        """Map days_remaining to (risk_level, hex_color)."""
        if days is None:
            return "Unknown", "#6B7280"     # Gray
        if days <= 0:
            return "High",    "#DC2626"     # Red   — overdue
        if days <= HIGH_THRESHOLD:
            return "High",    "#DC2626"     # Red
        if days <= MEDIUM_THRESHOLD:
            return "Medium",  "#D97706"     # Amber
        return "Low",         "#16A34A"     # Green

    @staticmethod
    def _aggregate_risk(items: List[Dict[str, Any]]) -> str:
        """
        Overall case risk = worst risk level across all deadlines.
        Priority: High > Medium > Low > Unknown
        """
        priority = {"High": 3, "Medium": 2, "Low": 1, "Unknown": 0}
        best = max(items, key=lambda x: priority.get(x.get("risk_level", "Unknown"), 0))
        return best.get("risk_level", "Unknown")

    @staticmethod
    def _summary(
        overall: str,
        flagged: List[Dict[str, Any]],
        all_items: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        color_map = {
            "High":    "#DC2626",
            "Medium":  "#D97706",
            "Low":     "#16A34A",
            "Unknown": "#6B7280",
        }
        return {
            "overall_risk":  overall,
            "risk_color":    color_map.get(overall, "#6B7280"),
            "flagged_items": flagged,
            "all_items":     all_items,
        }
