from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    staff = "staff"
    admin = "admin"


class TimeRange(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class RequestContext(BaseModel):
    requester_id: str = Field(..., description="Authenticated user identifier")
    requester_role: UserRole
    store_id: Optional[str] = Field(default=None, description="Optional caller store scope")


class BaseAPIResponse(BaseModel):
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    context: RequestContext
    message: str = Field(..., min_length=2, max_length=2000)
    as_of_date: date = Field(default_factory=date.today)


class ChatResponse(BaseAPIResponse):
    intent: str
    answer: str
    data: dict[str, Any]


class SummaryRequest(BaseModel):
    context: RequestContext
    time_range: TimeRange
    staff_id: Optional[str] = None
    store_id: Optional[str] = None
    as_of_date: date = Field(default_factory=date.today)


class SummaryResponse(BaseAPIResponse):
    summary_type: str
    narrative: str
    metrics: dict[str, Any]


class AnalyticsRequest(BaseModel):
    context: RequestContext
    metric: str = Field(..., examples=["commission", "sales", "target_gap", "underperforming_staff"])
    time_range: TimeRange
    staff_id: Optional[str] = None
    store_id: Optional[str] = None
    as_of_date: date = Field(default_factory=date.today)


class AnalyticsResponse(BaseAPIResponse):
    metric: str
    time_range: TimeRange
    values: dict[str, Any]


class AnomaliesRequest(BaseModel):
    context: RequestContext
    anomaly_type: str = Field(default="sales_commission_attendance")
    store_id: Optional[str] = None
    as_of_date: date = Field(default_factory=date.today)


class AnomalyItem(BaseModel):
    entity_type: str
    entity_id: str
    severity: str
    reason: str


class AnomaliesResponse(BaseAPIResponse):
    anomaly_type: str
    items: list[AnomalyItem]


class RecommendationsRequest(BaseModel):
    context: RequestContext
    goal: str = Field(..., examples=["increase_commission", "recover_store_target"])
    staff_id: Optional[str] = None
    store_id: Optional[str] = None
    as_of_date: date = Field(default_factory=date.today)


class RecommendationsResponse(BaseAPIResponse):
    goal: str
    recommendations: list[str]
    expected_impact_note: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
