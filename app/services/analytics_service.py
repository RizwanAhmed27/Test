from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from typing import Dict, List, Tuple

from app.data.seed import COMMISSION_RULES, SALES_TRANSACTIONS, STORES, TARGETS, USERS


class AnalyticsService:
    def _date_window(self, as_of: date, time_range: str) -> Tuple[date, date]:
        if time_range == "daily":
            return as_of, as_of
        if time_range == "weekly":
            start = as_of - timedelta(days=as_of.weekday())
            return start, as_of
        start = as_of.replace(day=1)
        return start, as_of

    def _filter_sales(self, start: date, end: date, staff_id: str | None = None, store_id: str | None = None) -> List[dict]:
        rows = []
        for row in SALES_TRANSACTIONS:
            business_date = date.fromisoformat(row["business_date"])
            if business_date < start or business_date > end:
                continue
            if staff_id and row["staff_id"] != staff_id:
                continue
            if store_id and row["store_id"] != store_id:
                continue
            rows.append(row)
        return rows

    def sales_total(self, as_of: date, time_range: str, staff_id: str | None = None, store_id: str | None = None) -> float:
        start, end = self._date_window(as_of, time_range)
        sales = self._filter_sales(start, end, staff_id=staff_id, store_id=store_id)
        return round(sum(row["amount"] for row in sales), 2)

    def commission_total(self, as_of: date, time_range: str, staff_id: str | None = None, store_id: str | None = None) -> float:
        start, end = self._date_window(as_of, time_range)
        sales = self._filter_sales(start, end, staff_id=staff_id, store_id=store_id)

        total = 0.0
        base_rate = COMMISSION_RULES["base_rate"]
        bonus_threshold = COMMISSION_RULES["bonus_threshold"]
        bonus_rate = COMMISSION_RULES["bonus_rate"]

        grouped: Dict[str, float] = defaultdict(float)
        for row in sales:
            grouped[row["staff_id"]] += row["amount"]

        for staff_sales in grouped.values():
            commission = staff_sales * base_rate
            if staff_sales >= bonus_threshold:
                commission += staff_sales * bonus_rate
            total += commission

        return round(total, 2)

    def weekly_target_gap(self, as_of: date, staff_id: str) -> dict:
        start = as_of - timedelta(days=as_of.weekday())
        target = next(
            (row for row in TARGETS if row["staff_id"] == staff_id and row["period"] == "weekly" and row["period_start"] == str(start)),
            None,
        )
        if not target:
            return {"target": 0.0, "current_sales": 0.0, "gap": 0.0}

        current_sales = self.sales_total(as_of, "weekly", staff_id=staff_id)
        gap = max(0.0, target["target_amount"] - current_sales)
        return {
            "target": target["target_amount"],
            "current_sales": current_sales,
            "gap": round(gap, 2),
        }

    def store_performance(self, as_of: date, store_id: str) -> dict:
        sales = self.sales_total(as_of, "weekly", store_id=store_id)
        target = STORES[store_id].weekly_target
        attainment = round((sales / target) * 100, 2) if target else 0.0
        return {"weekly_sales": sales, "weekly_target": target, "attainment_pct": attainment}

    def underperforming_staff(self, as_of: date, store_id: str, threshold_pct: float = 70.0) -> List[dict]:
        store_staff_ids = {user_id for user_id, user in USERS.items() if user.store_id == store_id and user.role == "staff"}
        staff_targets = [row for row in TARGETS if row["period"] == "weekly" and row["staff_id"] in store_staff_ids]
        output = []
        for row in staff_targets:
            staff_sales = self.sales_total(as_of, "weekly", staff_id=row["staff_id"], store_id=store_id)
            attainment = (staff_sales / row["target_amount"] * 100) if row["target_amount"] else 0.0
            if attainment < threshold_pct:
                output.append(
                    {
                        "staff_id": row["staff_id"],
                        "sales": round(staff_sales, 2),
                        "target": row["target_amount"],
                        "attainment_pct": round(attainment, 2),
                    }
                )
        return output
