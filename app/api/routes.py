from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AnalyticsRequest,
    AnalyticsResponse,
    AnomaliesRequest,
    AnomaliesResponse,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    RecommendationsRequest,
    RecommendationsResponse,
    SummaryRequest,
    SummaryResponse,
)
from app.services.container import services

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    from app.core.config import settings

    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    services.role_guard.validate_actor(payload.context)
    intent, answer, data = services.chat.respond(
        message=payload.message,
        requester_id=payload.context.requester_id,
        requester_role=payload.context.requester_role.value,
        as_of_date=payload.as_of_date,
    )
    return ChatResponse(intent=intent, answer=answer, data=data)


@router.post("/summary", response_model=SummaryResponse)
def summary(payload: SummaryRequest) -> SummaryResponse:
    services.role_guard.validate_actor(payload.context)
    resolved_store_id = payload.store_id or payload.context.store_id

    if payload.staff_id:
        services.role_guard.can_access_staff(payload.context, payload.staff_id)
    if resolved_store_id:
        services.role_guard.can_access_store(payload.context, resolved_store_id)

    narrative, metrics = services.summaries.build_summary(
        as_of=payload.as_of_date,
        time_range=payload.time_range.value,
        staff_id=payload.staff_id,
        store_id=resolved_store_id,
    )
    return SummaryResponse(summary_type=payload.time_range.value, narrative=narrative, metrics=metrics)


@router.post("/analytics", response_model=AnalyticsResponse)
def analytics(payload: AnalyticsRequest) -> AnalyticsResponse:
    services.role_guard.validate_actor(payload.context)
    resolved_store_id = payload.store_id or payload.context.store_id

    if payload.staff_id:
        services.role_guard.can_access_staff(payload.context, payload.staff_id)
    if resolved_store_id:
        services.role_guard.can_access_store(payload.context, resolved_store_id)

    if payload.metric == "commission":
        values = {
            "commission_total": services.analytics.commission_total(
                payload.as_of_date,
                payload.time_range.value,
                payload.staff_id,
                resolved_store_id,
            )
        }
    elif payload.metric == "sales":
        values = {
            "sales_total": services.analytics.sales_total(
                payload.as_of_date,
                payload.time_range.value,
                payload.staff_id,
                resolved_store_id,
            )
        }
    elif payload.metric == "target_gap":
        if not payload.staff_id:
            raise HTTPException(status_code=400, detail="staff_id required for target_gap")
        if payload.time_range.value != "weekly":
            raise HTTPException(status_code=400, detail="target_gap only supports weekly time_range")
        values = services.analytics.weekly_target_gap(payload.as_of_date, payload.staff_id)
    elif payload.metric == "underperforming_staff":
        if not resolved_store_id:
            raise HTTPException(status_code=400, detail="store_id required for underperforming_staff")
        values = {"staff": services.analytics.underperforming_staff(payload.as_of_date, resolved_store_id)}
    else:
        raise HTTPException(status_code=400, detail="Unsupported metric")

    return AnalyticsResponse(metric=payload.metric, time_range=payload.time_range, values=values)


@router.post("/anomalies", response_model=AnomaliesResponse)
def anomalies(payload: AnomaliesRequest) -> AnomaliesResponse:
    services.role_guard.validate_actor(payload.context)
    resolved_store_id = payload.store_id or payload.context.store_id

    if resolved_store_id:
        services.role_guard.can_access_store(payload.context, resolved_store_id)

    items = services.anomalies.detect(payload.as_of_date, resolved_store_id)
    return AnomaliesResponse(anomaly_type=payload.anomaly_type, items=items)


@router.post("/recommendations", response_model=RecommendationsResponse)
def recommendations(payload: RecommendationsRequest) -> RecommendationsResponse:
    services.role_guard.validate_actor(payload.context)
    resolved_store_id = payload.store_id or payload.context.store_id

    if payload.staff_id:
        services.role_guard.can_access_staff(payload.context, payload.staff_id)
    if resolved_store_id:
        services.role_guard.can_access_store(payload.context, resolved_store_id)

    recs, note = services.recommendations.recommend(
        as_of=payload.as_of_date,
        goal=payload.goal,
        staff_id=payload.staff_id,
        store_id=resolved_store_id,
    )
    return RecommendationsResponse(goal=payload.goal, recommendations=recs, expected_impact_note=note)
