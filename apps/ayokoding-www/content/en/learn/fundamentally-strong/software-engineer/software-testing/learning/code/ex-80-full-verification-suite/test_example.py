"""Example 80: One Feature, Every Gate -- TDD Units, a Property Test, Integration, All Green."""
# clamp() gets every gate this whole Advanced tier taught: a genuine red-then-green TDD history,
# a Hypothesis property test, a real-collaborator integration test, coverage, and mutation.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from hypothesis import given  # => co-20: the decorator that turns a function into a property test  # fmt: skip
from hypothesis import strategies as st  # => co-20: the input-generation vocabulary used below  # fmt: skip

from clamp import clamp  # => co-17: imports the SAME clamp() every tier below exercises  # fmt: skip

# ---- co-17 TDD unit tests: written FIRST, against a not-yet-correct clamp() (see the Run block) ----


def test_unit_clamp_below_range_returns_lo() -> None:  # => co-17: RED against a naive first draft  # fmt: skip
    assert (
        clamp(-5, 0, 10) == 0
    )  # => co-17: fails against `return value` -- proves the floor branch


def test_unit_clamp_above_range_returns_hi() -> None:  # => co-17: RED against that SAME first draft  # fmt: skip
    assert (
        clamp(15, 0, 10) == 10
    )  # => co-17: fails against `return value` -- proves the cap branch


def test_unit_clamp_within_range_returns_value_unchanged() -> (
    None
):  # => the ONE case a naive draft
    assert (
        clamp(5, 0, 10) == 5
    )  # => passes -- clamp() implemented as identity would satisfy THIS alone


# ---- co-18/co-20 property test: an invariant, checked over MANY generated inputs, not three ----


@given(  # => co-20: Hypothesis strategies GENERATE the (value, lo, hi) triples below  # fmt: skip
    value=st.floats(
        min_value=-1000, max_value=1000, allow_nan=False
    ),  # => co-20: any float in range  # fmt: skip
    lo=st.floats(
        min_value=-1000, max_value=0, allow_nan=False
    ),  # => co-20: always at or below zero  # fmt: skip
    hi=st.floats(
        min_value=0, max_value=1000, allow_nan=False
    ),  # => co-20: always at or above zero  # fmt: skip
)
def test_property_clamp_result_always_within_bounds(  # => co-18: ONE invariant, hundreds of cases  # fmt: skip
    value: float, lo: float, hi: float
) -> None:
    result = clamp(value, lo, hi)  # => co-18: the SAME clamp() the unit tests above check by hand  # fmt: skip
    assert lo <= result <= hi  # => co-18: the INVARIANT -- true for every one of Hypothesis's cases  # fmt: skip


# ---- co-23 integration test: a REAL collaborator (Thermostat) combined with clamp(), not stubbed ----


class Thermostat:  # => co-23: a real, stateful collaborator that DEPENDS on clamp()  # fmt: skip
    def __init__(self, min_temp: float, max_temp: float) -> None:  # => co-23: real bounds, stored  # fmt: skip
        self.min_temp = min_temp  # => co-23: the REAL floor this device enforces  # fmt: skip
        self.max_temp = max_temp  # => co-23: the REAL ceiling this device enforces  # fmt: skip
        self.setpoint = min_temp  # => starts at the floor, like a real device powering on  # fmt: skip

    def set_target(self, requested: float) -> float:  # => co-23: calls the REAL clamp(), unstubbed  # fmt: skip
        self.setpoint = clamp(requested, self.min_temp, self.max_temp)  # => co-23: no double involved  # fmt: skip
        return self.setpoint  # => co-23: hands back whatever clamp() genuinely produced  # fmt: skip


def test_integration_thermostat_uses_real_clamp_to_stay_in_bounds() -> (
    None
):  # => co-23: combined
    thermostat = Thermostat(min_temp=16.0, max_temp=28.0)  # => a REAL Thermostat, REAL bounds  # fmt: skip
    assert thermostat.set_target(35.0) == 28.0  # => co-23: clamp() genuinely capped an over-request  # fmt: skip
    assert thermostat.set_target(10.0) == 16.0  # => co-23: and genuinely floored an under-request  # fmt: skip
    assert thermostat.set_target(22.0) == 22.0  # => co-23: and left an in-range request alone  # fmt: skip
