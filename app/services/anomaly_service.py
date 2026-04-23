from __future__ import annotations

from collections import defaultdict
from datetime import date

from app.data.seed import ATTENDANCE, SALES_TRANSACTIONS
from app.services.anomaly_detection import detect_spike


class AnomalyService:
    def detect(self, as_of: date, store_id: str | None = None) -> list[dict]:
        items: list[dict] = []
        sales_by_staff: dict[str, list[tuple[date, float]]] = defaultdict(list)

        for row in SALES_TRANSACTIONS:
            if store_id and row["store_id"] != store_id:
                continue
            transaction_date = date.fromisoformat(row["business_date"])
            if transaction_date > as_of:
                continue
            sales_by_staff[row["staff_id"]].append((transaction_date, row["amount"]))

        for staff_id, dated_amounts in sales_by_staff.items():
            if len(dated_amounts) < 2:
                continue

            dated_amounts.sort(key=lambda item: item[0], reverse=True)
            latest_date, latest_amount = dated_amounts[0]
            trailing_values = [amount for _, amount in dated_amounts[1:]]
            spike_result = detect_spike(latest_amount, trailing_values)
            if not spike_result.is_anomaly:
                continue

            items.append(
                {
                    "entity_type": "staff",
                    "entity_id": staff_id,
                    "severity": "high",
                    "reason": (
                        f"Latest sales value {spike_result.latest:.2f} on {latest_date.isoformat()} is significantly "
                        f"above baseline average {spike_result.baseline_avg:.2f}."
                    ),
                }
            )

        absent_today = [a for a in ATTENDANCE if a["business_date"] == str(as_of) and a["status"] == "absent"]
        for row in absent_today:
            items.append(
                {
                    "entity_type": "staff",
                    "entity_id": row["staff_id"],
                    "severity": "medium",
                    "reason": "Absent on current business date; may affect target attainment.",
                }
            )

        return items
