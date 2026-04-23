from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SpikeCheckResult:
    is_anomaly: bool
    latest: float
    baseline_avg: float


def detect_spike(latest: float, trailing_values: list[float], multiplier: float = 1.8) -> SpikeCheckResult:
    if not trailing_values:
        return SpikeCheckResult(False, latest=latest, baseline_avg=0.0)

    baseline = sum(trailing_values) / len(trailing_values)
    if baseline <= 0:
        return SpikeCheckResult(False, latest=latest, baseline_avg=baseline)

    return SpikeCheckResult(is_anomaly=latest > baseline * multiplier, latest=latest, baseline_avg=baseline)
