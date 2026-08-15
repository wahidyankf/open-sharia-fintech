"""Offline, deterministic SRE teaching loop for fictional Harbor Checkout.

This example is intentionally not a monitoring agent: it accepts no external input, starts no
server, performs no network I/O, and changes no files or system state.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from statistics import mean
from typing import Final, Sequence


SLO_TARGET: Final[float] = 0.999
PAGE_BURN_RATE: Final[float] = 10.0
LATENCY_OBJECTIVE_MS: Final[int] = 500
WORKER_CAPACITY: Final[int] = 10


class AlertRoute(str, Enum):
    """The only routes this local teaching program may return."""

    SILENT = "silent"
    TICKET = "ticket"
    PAGE = "page"


@dataclass(frozen=True)
class RequestEvent:
    """One synthetic checkout outcome; request IDs are opaque non-secret teaching labels."""

    request_id: str
    latency_ms: int
    status_code: int
    busy_workers: int

    def is_good(self) -> bool:
        """Return the stated availability-and-latency SLI good-event predicate."""

        return 200 <= self.status_code < 500 and self.latency_ms <= LATENCY_OBJECTIVE_MS


@dataclass(frozen=True)
class SignalSummary:
    """The four golden signals for a fixed event window."""

    mean_latency_ms: float
    traffic: int
    errors: int
    saturation: float


@dataclass(frozen=True)
class SloSummary:
    """An inspectable SLI, budget, and burn calculation."""

    sli: float
    remaining_budget: float
    burn_rate: float


def summarize_signals(events: Sequence[RequestEvent]) -> SignalSummary:
    """Summarize a non-empty synthetic window without exporting any telemetry."""

    if not events:
        raise ValueError("events must contain at least one synthetic request")
    latencies: list[int] = [event.latency_ms for event in events]
    errors: int = sum(event.status_code >= 500 for event in events)
    peak_busy_workers: int = max(event.busy_workers for event in events)
    saturation: float = peak_busy_workers / WORKER_CAPACITY
    return SignalSummary(mean(latencies), len(events), errors, saturation)


def summarize_slo(events: Sequence[RequestEvent], slo_target: float) -> SloSummary:
    """Calculate an SLI and budget state for a target strictly between zero and one."""

    if not 0.0 < slo_target < 1.0:
        raise ValueError("slo_target must be strictly between 0 and 1")
    if not events:
        raise ValueError("events must contain at least one synthetic request")
    good_events: int = sum(event.is_good() for event in events)
    sli: float = good_events / len(events)
    budget_fraction: float = 1.0 - slo_target
    observed_bad_fraction: float = 1.0 - sli
    remaining_budget: float = max(0.0, 1.0 - observed_bad_fraction / budget_fraction)
    burn_rate: float = observed_bad_fraction / budget_fraction
    return SloSummary(sli, remaining_budget, burn_rate)


def classify_alert(slo: SloSummary, signals: SignalSummary) -> AlertRoute:
    """Route user-impacting high burn to a page and lower actionable burn to a ticket."""

    if signals.errors > 0 and slo.burn_rate >= PAGE_BURN_RATE:
        return AlertRoute.PAGE
    if signals.saturation >= 0.9 or slo.burn_rate > 1.0:
        return AlertRoute.TICKET
    return AlertRoute.SILENT


HEALTHY_EVENTS: Final[tuple[RequestEvent, ...]] = (
    RequestEvent("sample-001", 120, 200, 4),
    RequestEvent("sample-002", 180, 200, 5),
    RequestEvent("sample-003", 240, 200, 5),
    RequestEvent("sample-004", 300, 200, 6),
)

INCIDENT_EVENTS: Final[tuple[RequestEvent, ...]] = HEALTHY_EVENTS + (
    RequestEvent("sample-005", 900, 503, 9),
    RequestEvent("sample-006", 1_100, 503, 10),
    RequestEvent("sample-007", 800, 503, 10),
    RequestEvent("sample-008", 950, 503, 10),
)


def main() -> None:
    """Run fixed fixtures and print only derived teaching outputs."""

    healthy_signals: SignalSummary = summarize_signals(HEALTHY_EVENTS)
    healthy_slo: SloSummary = summarize_slo(HEALTHY_EVENTS, SLO_TARGET)
    incident_signals: SignalSummary = summarize_signals(INCIDENT_EVENTS)
    incident_slo: SloSummary = summarize_slo(INCIDENT_EVENTS, SLO_TARGET)
    assert classify_alert(healthy_slo, healthy_signals) is AlertRoute.SILENT
    assert classify_alert(incident_slo, incident_signals) is AlertRoute.PAGE
    assert incident_signals.saturation == 1.0
    print(f"healthy route: {classify_alert(healthy_slo, healthy_signals)}")
    print(f"incident signals: {incident_signals}")
    print(f"incident SLO: {incident_slo}")
    print(f"incident route: {classify_alert(incident_slo, incident_signals)}")


if __name__ == "__main__":
    main()
