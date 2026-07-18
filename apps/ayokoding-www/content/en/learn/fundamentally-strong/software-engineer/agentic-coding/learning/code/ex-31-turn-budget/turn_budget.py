# learning/code/ex-31-turn-budget/turn_budget.py
"""Example 31: A TurnBudget That Halts Once a Token Ceiling Is Crossed."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-18: a typed, self-documenting record for cumulative spend + history


class BudgetExceededError(RuntimeError):  # => co-18: a dedicated exception type -- callers can catch THIS, not a bare RuntimeError
    """Raised when a session's cumulative token spend crosses its configured ceiling."""  # => co-18: documents BudgetExceededError's contract -- no runtime output, just sets its __doc__


@dataclass  # => co-18: mutable record -- spent/history change turn by turn, unlike the frozen records elsewhere in this topic
class TurnBudget:  # => co-18: the tripwire itself -- halts a session once its ceiling is crossed
    """Tracks cumulative token spend across turns; raises once the ceiling is crossed."""  # => co-18: documents TurnBudget's contract -- no runtime output, just sets its __doc__

    ceiling: int  # => co-18: the stated budget ceiling, set BEFORE the session starts
    spent: int = 0  # => co-18: running total, starts at zero
    history: list[tuple[int, int]] = field(default_factory=list[tuple[int, int]])  # => co-18: (turn_number, tokens_this_turn) -- an audit trail of every recorded turn

    def record_turn(self, turn_number: int, tokens: int) -> None:  # => co-18: called once per turn, in order
        """Record one turn's token spend; raise BudgetExceededError if it crosses the ceiling."""  # => co-18: documents record_turn's contract -- no runtime output, just sets its __doc__
        self.spent += tokens  # => co-18: cumulative spend grows by this turn's cost
        self.history.append((turn_number, tokens))  # => co-18: recorded BEFORE the raise -- the halting turn's spend stays auditable
        if self.spent > self.ceiling:  # => co-18: the ONE condition this whole example demonstrates
            raise BudgetExceededError(  # => co-18: halts the session -- the caller cannot silently continue past this
                f"turn {turn_number} pushed cumulative spend to {self.spent}, "  # => co-18: names the exact turn and the new cumulative total
                f"exceeding the ceiling of {self.ceiling}"  # => co-18: names the configured ceiling that was crossed
            )  # => co-18: closes the multi-line construct opened above


if __name__ == "__main__":  # => co-18: entry point -- this block runs only when the file executes directly, not on import
    budget = TurnBudget(ceiling=10_000)  # => co-18: a stated budget ceiling, fixed before the session begins
    turns = [(1, 2_500), (2, 3_000), (3, 2_800), (4, 4_000), (5, 1_000)]  # => co-18: turn 4 is DESIGNED to cross the ceiling
    halted_at = None  # => co-18: records which turn actually triggered the halt, if any
    for turn_number, tokens in turns:  # => co-18: processes turns strictly in order -- turn 5 must never run if turn 4 halts
        try:  # => co-18: only the halting turn is expected to raise
            budget.record_turn(turn_number, tokens)  # => co-18: records this turn's spend against the running total
            print(f"turn {turn_number}: +{tokens} tokens, cumulative={budget.spent}")  # => co-18: this turn completed under budget
        except BudgetExceededError as exc:  # => co-18: the expected halt condition firing
            halted_at = turn_number  # => co-18: records the exact turn that crossed the ceiling
            print(f"turn {turn_number}: HALTED -- {exc}")  # => co-18: the captured halt message
            break  # => co-18: stops the loop -- turn 5 is intentionally never reached

    assert halted_at == 4, "the session must halt exactly at turn 4"  # => co-18: 2500+3000+2800+4000=12300 > 10000
    assert budget.history[-1] == (4, 4000), "the halting turn's spend must still be recorded"  # => co-18: the audit trail survives the raise
    assert len(budget.history) == 4, "turn 5 must never run once the halt fires"  # => co-18: proves the break above actually worked
    print("Session halted at turn 4, before turn 5 could run: True")  # => co-18: this file is self-verifying -- a clean exit proves the claim held
