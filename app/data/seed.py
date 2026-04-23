from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, List


@dataclass(frozen=True)
class SeedStore:
    store_id: str
    name: str
    weekly_target: float


@dataclass(frozen=True)
class SeedUser:
    user_id: str
    role: str
    name: str
    store_id: str


TODAY = date.today()
THIS_WEEK_START = TODAY - timedelta(days=TODAY.weekday())

STORES: Dict[str, SeedStore] = {
    "s1": SeedStore(store_id="s1", name="Downtown", weekly_target=12000.0),
    "s2": SeedStore(store_id="s2", name="Mall", weekly_target=9000.0),
}

USERS: Dict[str, SeedUser] = {
    "staff_anna": SeedUser(user_id="staff_anna", role="staff", name="Anna", store_id="s1"),
    "staff_liam": SeedUser(user_id="staff_liam", role="staff", name="Liam", store_id="s1"),
    "staff_noor": SeedUser(user_id="staff_noor", role="staff", name="Noor", store_id="s2"),
    "mgr_s1": SeedUser(user_id="mgr_s1", role="admin", name="Maria", store_id="s1"),
    "admin_root": SeedUser(user_id="admin_root", role="admin", name="Root Admin", store_id="s1"),
}

SALES_TRANSACTIONS: List[dict] = [
    {"transaction_id": "t1", "staff_id": "staff_anna", "store_id": "s1", "amount": 520.0, "business_date": str(TODAY)},
    {"transaction_id": "t2", "staff_id": "staff_anna", "store_id": "s1", "amount": 380.0, "business_date": str(TODAY)},
    {"transaction_id": "t3", "staff_id": "staff_liam", "store_id": "s1", "amount": 180.0, "business_date": str(TODAY)},
    {"transaction_id": "t4", "staff_id": "staff_noor", "store_id": "s2", "amount": 260.0, "business_date": str(TODAY)},
    {"transaction_id": "t5", "staff_id": "staff_anna", "store_id": "s1", "amount": 3000.0, "business_date": str(TODAY - timedelta(days=2))},
    {"transaction_id": "t6", "staff_id": "staff_liam", "store_id": "s1", "amount": 1400.0, "business_date": str(TODAY - timedelta(days=3))},
    {"transaction_id": "t7", "staff_id": "staff_noor", "store_id": "s2", "amount": 2500.0, "business_date": str(TODAY - timedelta(days=1))},
]

ATTENDANCE: List[dict] = [
    {"attendance_id": "a1", "staff_id": "staff_anna", "business_date": str(TODAY), "status": "present", "hours": 8.0},
    {"attendance_id": "a2", "staff_id": "staff_liam", "business_date": str(TODAY), "status": "present", "hours": 6.0},
    {"attendance_id": "a3", "staff_id": "staff_noor", "business_date": str(TODAY), "status": "absent", "hours": 0.0},
]

COMMISSION_RULES: Dict[str, float] = {
    "base_rate": 0.05,
    "bonus_threshold": 2000.0,
    "bonus_rate": 0.02,
}

TARGETS: List[dict] = [
    {"target_id": "tg1", "staff_id": "staff_anna", "period": "weekly", "period_start": str(THIS_WEEK_START), "target_amount": 4500.0},
    {"target_id": "tg2", "staff_id": "staff_liam", "period": "weekly", "period_start": str(THIS_WEEK_START), "target_amount": 4000.0},
    {"target_id": "tg3", "staff_id": "staff_noor", "period": "weekly", "period_start": str(THIS_WEEK_START), "target_amount": 3500.0},
]
