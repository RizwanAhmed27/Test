from __future__ import annotations

from datetime import date

from app.services.analytics_service import AnalyticsService


class RecommendationService:
    def __init__(self, analytics: AnalyticsService) -> None:
        self.analytics = analytics

    def recommend(self, as_of: date, goal: str, staff_id: str | None = None, store_id: str | None = None) -> tuple[list[str], str]:
        if goal == "increase_commission" and staff_id:
            gap_data = self.analytics.weekly_target_gap(as_of, staff_id)
            gap = gap_data["gap"]
            recs = [
                "Prioritize high-ticket items in the next two shifts.",
                "Run add-on bundle prompts on every qualifying checkout.",
                "Focus on peak-hour conversion windows and reduce low-intent interactions.",
            ]
            note = f"Remaining weekly sales gap is {gap:.2f}; actions are ranked to improve conversion and commission quickly."
            return recs, note

        if goal == "recover_store_target" and store_id:
            perf = self.analytics.store_performance(as_of, store_id)
            recs = [
                "Reallocate top converters to peak traffic blocks.",
                "Trigger a short-duration promo on high-margin SKUs.",
                "Coach bottom quartile staff using yesterday's missed opportunities.",
            ]
            note = f"Store attainment is {perf['attainment_pct']:.2f}% of weekly target; recommendations focus on immediate lift."
            return recs, note

        return ["Provide a supported goal with required context (staff_id or store_id)."], "Insufficient context to generate actionable recommendation."
