from __future__ import annotations


class IntentRouterService:
    def detect_intent(self, message: str) -> str:
        lowered = message.lower()
        if "commission" in lowered and "today" in lowered:
            return "commission_lookup"
        if "need" in lowered and "this week" in lowered:
            return "target_gap_planning"
        if "summary" in lowered or "summarise" in lowered:
            return "performance_summary"
        if "unusual" in lowered or "anomaly" in lowered:
            return "anomaly_review"
        if "underperform" in lowered:
            return "underperformance_detection"
        if "behind target" in lowered:
            return "store_target_diagnosis"
        return "general_kpi_question"
