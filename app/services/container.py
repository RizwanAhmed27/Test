from __future__ import annotations

from app.services.analytics_service import AnalyticsService
from app.services.anomaly_service import AnomalyService
from app.services.chat_service import ChatService
from app.services.intent_router import IntentRouterService
from app.services.recommendation_service import RecommendationService
from app.services.role_guard import RoleGuardService
from app.services.summary_service import SummaryService


class ServiceContainer:
    def __init__(self) -> None:
        self.role_guard = RoleGuardService()
        self.analytics = AnalyticsService()
        self.summaries = SummaryService(self.analytics)
        self.recommendations = RecommendationService(self.analytics)
        self.anomalies = AnomalyService()
        self.intent_router = IntentRouterService()
        self.chat = ChatService(
            intent_router=self.intent_router,
            analytics=self.analytics,
            summaries=self.summaries,
            recommendations=self.recommendations,
            anomalies=self.anomalies,
        )


services = ServiceContainer()
