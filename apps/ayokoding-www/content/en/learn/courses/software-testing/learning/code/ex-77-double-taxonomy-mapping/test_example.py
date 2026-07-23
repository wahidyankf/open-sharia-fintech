"""Example 77: One Scenario, Five Doubles -- Dummy, Stub, Spy, Mock, and Fake, Meszaros-Precise."""

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from unittest.mock import MagicMock  # => co-12/co-13/co-15: the double type behind three of the five roles  # fmt: skip


class RealAuditLog:  # => a REAL collaborator -- the spy below WRAPS this, it doesn't replace it  # fmt: skip
    def __init__(self) -> None:  # => starts with an empty log, genuinely  # fmt: skip
        self.entries: list[str] = []  # => co-15: REAL state the spy's wrapped calls actually mutate  # fmt: skip

    def record(self, message: str) -> None:  # => co-15: genuinely appends -- the spy lets this RUN  # fmt: skip
        self.entries.append(message)  # => co-15: the REAL side effect a spy preserves  # fmt: skip


class FakeRepository:  # => co-16: a WORKING lightweight implementation, not a mock of one  # fmt: skip
    """An in-memory stand-in for a real database -- genuinely stores and returns data."""  # => co-16

    def __init__(self) -> None:  # => starts empty, with real, genuine state  # fmt: skip
        self._rows: dict[int, tuple[str, int, float]] = {}  # => co-16: REAL storage, not a mock  # fmt: skip
        self._next_id = 1  # => co-16: REAL id generation, like a genuine repository would do  # fmt: skip

    def save(self, sku: str, quantity: int, total: float) -> int:  # => co-16: REAL working logic  # fmt: skip
        order_id = self._next_id  # => co-16: the REAL id assigned to this row  # fmt: skip
        self._rows[order_id] = (sku, quantity, total)  # => genuinely stored, retrievable below  # fmt: skip
        self._next_id += 1  # => co-16: REAL id increment for the NEXT save() call  # fmt: skip
        return order_id  # => co-16: hands back the REAL, genuinely assigned id  # fmt: skip

    def get(self, order_id: int) -> tuple[str, int, float]:  # => co-16: genuinely reads it back  # fmt: skip
        return self._rows[order_id]  # => co-16: a REAL read from REAL, if lightweight, storage  # fmt: skip


class OrderProcessor:  # => the unit under test -- FIVE collaborators, FIVE different double roles  # fmt: skip
    def __init__(
        self,
        price_lookup: object,  # => co-12: the STUB -- returns a canned price  # fmt: skip
        notifier: object,  # => co-13: the MOCK -- its call gets VERIFIED below  # fmt: skip
        audit_log: object,  # => co-15: the SPY -- wraps a real AuditLog, delegates AND records  # fmt: skip
        repository: FakeRepository,  # => co-16: the FAKE -- a real, working, lightweight impl  # fmt: skip
        logger: object,  # => co-11: the DUMMY -- accepted, stored, but NEVER called below  # fmt: skip
    ) -> None:
        self.price_lookup = price_lookup  # => co-12: stored for process() to call below  # fmt: skip
        self.notifier = notifier  # => co-13: stored for process() to call below  # fmt: skip
        self.audit_log = audit_log  # => co-15: stored for process() to call below  # fmt: skip
        self.repository = repository  # => co-16: stored for process() to call below  # fmt: skip
        self.logger = logger  # => co-11: stored only to satisfy the constructor's signature  # fmt: skip

    def process(self, sku: str, quantity: int) -> tuple[int, float]:  # => the ONE method exercised  # fmt: skip
        price = self.price_lookup.price_for(sku)  # type: ignore[attr-defined]  # => co-12: STUB call
        total = price * quantity  # => co-01: combines the STUB's canned price with a real quantity  # fmt: skip
        order_id = self.repository.save(sku, quantity, total)  # => co-16: FAKE's REAL logic runs  # fmt: skip
        self.notifier.notify(order_id, total)  # type: ignore[attr-defined]  # => co-13: MOCK call  # fmt: skip
        self.audit_log.record(f"order {order_id} processed")  # type: ignore[attr-defined]  # => co-15
        # self.logger is NEVER touched anywhere in this method -- that omission IS the dummy's point
        return order_id, total  # => co-01: the REAL result callers use, built from all five doubles  # fmt: skip


def test_five_doubles_one_scenario_each_matching_its_meszaros_role() -> (
    None
):  # => co-11/12/13/15/16
    # --- co-12 STUB: returns a CANNED answer, regardless of what's asked ---
    stub_price_lookup = MagicMock()  # => co-12: a bare MagicMock, used purely as a STUB  # fmt: skip
    stub_price_lookup.price_for.return_value = 9.99  # => co-12: the SAME canned value every time  # fmt: skip

    # --- co-13 MOCK: its INTERACTION is what gets verified, not just a return value ---
    mock_notifier = MagicMock()  # => co-13: no return value configured -- ONLY the call matters  # fmt: skip

    # --- co-15 SPY: wraps a REAL object, so real behavior STILL happens, AND calls are recorded ---
    real_audit_log = RealAuditLog()  # => co-15: the genuine collaborator being spied ON  # fmt: skip
    spy_audit_log = MagicMock(wraps=real_audit_log)  # => co-15: delegates to real_audit_log.record()  # fmt: skip

    # --- co-16 FAKE: a REAL, working implementation -- not a MagicMock at all ---
    fake_repository = FakeRepository()  # => co-16: genuinely stores/retrieves, no mocking involved  # fmt: skip

    # --- co-11 DUMMY: passed to satisfy the signature, never invoked, never asserted on ---
    dummy_logger = object()  # => co-11: not even a MagicMock -- proves it is TRULY never called  # fmt: skip

    processor = OrderProcessor(  # => arrange: ONE processor, FIVE doubles, each a different role  # fmt: skip
        stub_price_lookup, mock_notifier, spy_audit_log, fake_repository, dummy_logger
    )
    order_id, total = processor.process("widget", 3)  # => the ONE call exercising all FIVE doubles  # fmt: skip

    # co-12 STUB verification: the RESULT reflects the canned answer -- state-based, not call-based.
    assert total == 29.97  # => 9.99 * 3, proving the stub's canned value was genuinely used  # fmt: skip

    # co-13 MOCK verification: the INTERACTION itself is asserted -- behavior-based, not state-based.
    mock_notifier.notify.assert_called_once_with(order_id, 29.97)  # => co-13: exact call, verified  # fmt: skip

    # co-15 SPY verification: BOTH the real side effect AND the call are checked.
    assert real_audit_log.entries == [f"order {order_id} processed"]  # => co-15: REAL delegation ran  # fmt: skip
    spy_audit_log.record.assert_called_once()  # => co-15: AND the call itself was recorded  # fmt: skip

    # co-16 FAKE verification: read the REAL (if lightweight) state back out.
    assert fake_repository.get(order_id) == ("widget", 3, 29.97)  # => co-16: genuinely persisted  # fmt: skip

    # co-11 DUMMY verification: this test makes NO assertion about dummy_logger at all -- that
    # ABSENCE of any call/assertion is precisely what makes it a dummy, not a stub or a mock.
