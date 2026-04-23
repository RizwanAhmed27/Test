from __future__ import annotations

from datetime import date

from app.services.analytics_service import AnalyticsService


class SummaryService:
    def __init__(self, analytics: AnalyticsService) -> None:
        self.analytics = analytics

    def build_summary(self, as_of: date, time_range: str, staff_id: str | None, store_id: str | None) -> tuple[str, dict]:
        sales = self.analytics.sales_total(as_of, time_range, staff_id=staff_id, store_id=store_id)
        commission = self.analytics.commission_total(as_of, time_range, staff_id=staff_id, store_id=store_id)
        metrics = {
            "sales_total": sales,
            "commission_total": commission,
            "time_range": time_range,
            "as_of_date": str(as_of),
        }
        if staff_id:
            narrative = (
                f"Performance summary for {staff_id}: sales are {sales:.2f} and estimated commission is {commission:.2f} "
                f"for the selected {time_range} period."
            )
        elif store_id:
            perf = self.analytics.store_performance(as_of, store_id)
            metrics.update(perf)
            narrative = (
                f"Store {store_id} is at {perf['attainment_pct']:.2f}% of weekly target. "
                f"Current weekly sales: {perf['weekly_sales']:.2f} vs target {perf['weekly_target']:.2f}."
            )
        else:
            narrative = "Summary generated for current scope."

        return narrative, metrics
