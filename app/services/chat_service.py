from __future__ import annotations

from datetime import date

from app.services.analytics_service import AnalyticsService
from app.services.anomaly_service import AnomalyService
from app.services.intent_router import IntentRouterService
from app.services.recommendation_service import RecommendationService
from app.services.summary_service import SummaryService


class ChatService:
    def __init__(
        self,
        intent_router: IntentRouterService,
        analytics: AnalyticsService,
        summaries: SummaryService,
        recommendations: RecommendationService,
        anomalies: AnomalyService,
    ) -> None:
        self.intent_router = intent_router
        self.analytics = analytics
        self.summaries = summaries
        self.recommendations = recommendations
        self.anomalies = anomalies

    def respond(self, message: str, requester_id: str, requester_role: str, as_of_date: date) -> tuple[str, str, dict]:
        intent = self.intent_router.detect_intent(message)

        if intent == "commission_lookup":
            total = self.analytics.commission_total(as_of_date, "daily", staff_id=requester_id if requester_role == "staff" else None)
            answer = f"Estimated commission for today is {total:.2f}."
            return intent, answer, {"commission_total": total, "time_range": "daily"}

        if intent == "target_gap_planning" and requester_role == "staff":
            gap = self.analytics.weekly_target_gap(as_of_date, requester_id)
            needed = gap["gap"]
            answer = f"You need {needed:.2f} more in sales this week to hit your target."
            return intent, answer, gap

        if intent == "performance_summary":
            narrative, metrics = self.summaries.build_summary(as_of_date, "daily", staff_id=requester_id if requester_role == "staff" else None, store_id=None)
            return intent, narrative, metrics

        if intent == "anomaly_review":
            items = self.anomalies.detect(as_of_date)
            answer = "Found unusual activity." if items else "No unusual activity detected."
            return intent, answer, {"anomalies": items}

        if intent == "store_target_diagnosis":
            answer = "For diagnosis, use /summary or /analytics with store_id for structured details."
            return intent, answer, {}

        if intent == "underperformance_detection" and requester_role == "admin":
            answer = "Use /analytics with metric=underperforming_staff and a store_id to list underperformers."
            return intent, answer, {"metric": "underperforming_staff"}

        recs, note = self.recommendations.recommend(as_of_date, "increase_commission", staff_id=requester_id)
        answer = f"Recommended actions: {' '.join(recs)}"
        return intent, answer, {"recommendation_note": note}
