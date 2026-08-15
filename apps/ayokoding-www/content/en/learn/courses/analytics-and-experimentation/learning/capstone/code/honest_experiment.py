"""Safe, offline analytics-and-experimentation capstone for fictional Lantern Notes.

The program uses fixed synthetic data and an in-memory SQLite database. It accepts no external
input, makes no network calls, and does not create or change persistent files or services.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import ceil, exp, sqrt
from sqlite3 import Connection, connect
from statistics import NormalDist
from typing import Final, Literal, Sequence


Arm = Literal["control", "treatment"]
Decision = Literal["SHIP", "NO_SHIP_EFFECT", "NO_SHIP_GUARDRAIL", "ABORT_SRM"]
NORMAL: Final[NormalDist] = NormalDist()
ALPHA: Final[float] = 0.05


@dataclass(frozen=True)
class TrackingEvent:
    """A minimal reviewed tracking contract; IDs are opaque synthetic labels."""

    event_id: str
    user_id: str
    event_name: str
    occurred_on: str
    platform: str


@dataclass(frozen=True)
class ExperimentPlan:
    """All inputs approved before an experiment result is examined."""

    salt: str
    baseline_rate: float
    minimum_detectable_effect: float
    guardrail_p95_limit_ms: int


@dataclass(frozen=True)
class ArmOutcome:
    """Aggregate binary outcome and a latency guardrail reading for one arm."""

    assigned_users: int
    conversions: int
    p95_latency_ms: int

    def conversion_rate(self) -> float:
        """Return the additive conversion numerator divided by its assigned denominator."""

        return self.conversions / self.assigned_users


@dataclass(frozen=True)
class ExperimentResult:
    """An effect result that keeps uncertainty and integrity checks visible."""

    lift: float
    ci_low: float
    ci_high: float
    p_value: float
    srm_p_value: float
    decision: Decision


EVENTS: Final[tuple[TrackingEvent, ...]] = (
    TrackingEvent("view-1", "user-1", "note_viewed", "2026-08-03", "web"),
    TrackingEvent("start-1", "user-1", "edit_started", "2026-08-03", "web"),
    TrackingEvent("save-1", "user-1", "edit_saved", "2026-08-03", "web"),
    TrackingEvent("view-2", "user-2", "note_viewed", "2026-08-03", "ios"),
    TrackingEvent("start-2", "user-2", "edit_started", "2026-08-03", "ios"),
    TrackingEvent("view-3", "user-3", "note_viewed", "2026-08-10", "android"),
    TrackingEvent("view-4", "user-4", "note_viewed", "2026-08-10", "web"),
    TrackingEvent("start-4", "user-4", "edit_started", "2026-08-10", "web"),
    TrackingEvent("save-4", "user-4", "edit_saved", "2026-08-11", "web"),
    TrackingEvent("save-4", "user-4", "edit_saved", "2026-08-11", "web"),  # retry
)
PLAN: Final[ExperimentPlan] = ExperimentPlan("editor-layout-v1", 0.12, 0.02, 500)


def write_events(connection: Connection, events: Sequence[TrackingEvent]) -> int:
    """Insert events idempotently into an in-memory table and return its deduplicated row count."""

    connection.execute(
        "CREATE TABLE events (event_id TEXT PRIMARY KEY, user_id TEXT, event_name TEXT, occurred_on TEXT, platform TEXT)"
    )
    connection.executemany(
        "INSERT OR IGNORE INTO events VALUES (?, ?, ?, ?, ?)",
        [(event.event_id, event.user_id, event.event_name, event.occurred_on, event.platform) for event in events],
    )
    row_count: int = int(connection.execute("SELECT COUNT(*) FROM events").fetchone()[0])
    return row_count


def deduplicated_events(events: Sequence[TrackingEvent]) -> tuple[TrackingEvent, ...]:
    """Return one event per stable event ID, preserving the first emitted business fact."""

    unique: dict[str, TrackingEvent] = {}
    for event in events:
        unique.setdefault(event.event_id, event)
    return tuple(unique.values())


def funnel(events: Sequence[TrackingEvent]) -> tuple[int, int, int]:
    """Count distinct users at ordered view, start, and save steps."""

    viewed: set[str] = {event.user_id for event in events if event.event_name == "note_viewed"}
    started: set[str] = {event.user_id for event in events if event.event_name == "edit_started"}
    saved: set[str] = {event.user_id for event in events if event.event_name == "edit_saved"}
    return len(viewed), len(started), len(saved)


def day_one_retention(events: Sequence[TrackingEvent]) -> float:
    """Return original-cohort users active on the next calendar day in this tiny fixture."""

    cohort: set[str] = {event.user_id for event in events if event.occurred_on == "2026-08-10"}
    returned: set[str] = {
        event.user_id for event in events if event.occurred_on == "2026-08-11" and event.user_id in cohort
    }
    return len(returned) / len(cohort)


def assign(user_id: str, salt: str) -> Arm:
    """Map a user persistently to one 50/50 arm without treatment-dependent inputs."""

    digest: bytes = sha256(f"{salt}:{user_id}".encode("utf-8")).digest()
    return "control" if int.from_bytes(digest[:8], "big") % 100 < 50 else "treatment"


def required_per_arm(plan: ExperimentPlan) -> int:
    """Use the course's approximate 80%-power planning formula for a binary baseline."""

    variance: float = plan.baseline_rate * (1.0 - plan.baseline_rate)
    return ceil(16.0 * variance / plan.minimum_detectable_effect**2)


def srm_p_value(control_count: int, treatment_count: int) -> float:
    """Return the df=1 chi-square survival probability for a 50/50 expected split."""

    total: int = control_count + treatment_count
    expected: float = total / 2.0
    chi_square: float = ((control_count - expected) ** 2 + (treatment_count - expected) ** 2) / expected
    return exp(-chi_square / 2.0)


def analyze(control: ArmOutcome, treatment: ArmOutcome, plan: ExperimentPlan) -> ExperimentResult:
    """Calculate a fixed-horizon two-proportion result and apply integrity-first decision gates."""

    control_rate: float = control.conversion_rate()
    treatment_rate: float = treatment.conversion_rate()
    lift: float = treatment_rate - control_rate
    standard_error: float = sqrt(
        control_rate * (1.0 - control_rate) / control.assigned_users
        + treatment_rate * (1.0 - treatment_rate) / treatment.assigned_users
    )
    z_value: float = lift / standard_error if standard_error else 0.0
    p_value: float = 2.0 * (1.0 - NORMAL.cdf(abs(z_value)))
    margin: float = NORMAL.inv_cdf(1.0 - ALPHA / 2.0) * standard_error
    srm: float = srm_p_value(control.assigned_users, treatment.assigned_users)
    if srm < ALPHA:
        decision: Decision = "ABORT_SRM"
    elif treatment.p95_latency_ms > plan.guardrail_p95_limit_ms:
        decision = "NO_SHIP_GUARDRAIL"
    elif p_value < ALPHA and (lift - margin) >= plan.minimum_detectable_effect:
        decision = "SHIP"
    else:
        decision = "NO_SHIP_EFFECT"
    return ExperimentResult(lift, lift - margin, lift + margin, p_value, srm, decision)


def main() -> None:
    """Run fixed fixtures and print only derived teaching evidence."""

    with connect(":memory:") as connection:
        stored_rows: int = write_events(connection, EVENTS)
    unique_events: tuple[TrackingEvent, ...] = deduplicated_events(EVENTS)
    funnel_counts: tuple[int, int, int] = funnel(unique_events)
    retention: float = day_one_retention(unique_events)
    assignments: tuple[Arm, ...] = tuple(assign(f"user-{number}", PLAN.salt) for number in range(2_000))
    control_count: int = assignments.count("control")
    treatment_count: int = assignments.count("treatment")
    result: ExperimentResult = analyze(ArmOutcome(800, 96, 420), ArmOutcome(800, 144, 560), PLAN)
    null_result: ExperimentResult = analyze(ArmOutcome(800, 80, 420), ArmOutcome(800, 80, 420), PLAN)

    assert stored_rows == 9
    assert funnel_counts == (4, 3, 2)
    assert funnel_counts[0] >= funnel_counts[1] >= funnel_counts[2]
    assert retention == 0.5
    assert assign("user-42", PLAN.salt) == assign("user-42", PLAN.salt)
    assert abs(control_count - treatment_count) < 100
    assert result.srm_p_value >= ALPHA
    assert result.decision == "NO_SHIP_GUARDRAIL"
    assert null_result.p_value == 1.0
    assert null_result.ci_low <= 0.0 <= null_result.ci_high
    print(f"deduplicated event rows: {stored_rows}")
    print(f"funnel view/start/save: {funnel_counts}")
    print(f"day-1 retention: {retention:.0%}")
    print(f"planned users per arm: {required_per_arm(PLAN)}")
    print(f"assignment control/treatment: {control_count}/{treatment_count}")
    print(f"lift: {result.lift:.2%}; 95% CI: [{result.ci_low:.2%}, {result.ci_high:.2%}]")
    print(f"two-sided p-value: {result.p_value:.4f}; SRM p-value: {result.srm_p_value:.4f}")
    print(f"decision: {result.decision}")
    print(f"known-null p-value: {null_result.p_value:.4f}")


if __name__ == "__main__":
    main()
