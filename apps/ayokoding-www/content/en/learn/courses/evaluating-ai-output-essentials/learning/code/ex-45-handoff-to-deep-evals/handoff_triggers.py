# learning/code/ex-45-handoff-to-deep-evals/handoff_triggers.py
"""Worked Example 45: Handoff to Deep Evals."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import NamedTuple  # => co-12: a typed record for one concrete graduation trigger


class Trigger(NamedTuple):  # => co-12: one concrete condition that means "this course is out of road"
    condition: str  # => co-12: the exact, checkable condition
    met: bool  # => co-12: whether THIS scenario's project has hit it


PROJECT_STATE = {  # => co-12: a real snapshot of a hypothetical project's current situation
    "wants_subjective_scoring": True,  # => co-12: someone is asking to score tone/faithfulness, not just facts
    "needs_failure_root_cause": True,  # => co-12: someone is asking WHY cases fail, not just which ones
    "case_count": 11,  # => co-12: still well under a large-scale eval suite
    "wants_ci_auto_block": False,  # => co-12: nobody has asked for unattended CI gating -- yet
}  # => co-12: closes PROJECT_STATE
TRIGGERS = [  # => co-12: three concrete triggers, each derived directly from PROJECT_STATE
    Trigger("a stakeholder wants a SUBJECTIVE quality scored", bool(PROJECT_STATE["wants_subjective_scoring"])),  # => co-12: trigger 1 -- bool() because PROJECT_STATE also holds an int (case_count), so lookups infer bool | int
    Trigger("someone asks WHY cases fail, not just WHICH", bool(PROJECT_STATE["needs_failure_root_cause"])),  # => co-12: trigger 2
    Trigger("the team wants CI to auto-block a merge on eval failure", bool(PROJECT_STATE["wants_ci_auto_block"])),  # => co-12: trigger 3
]  # => co-12: closes TRIGGERS


if __name__ == "__main__":  # => co-12: entry point -- runs only when this file executes directly, not on import
    print("Graduation triggers for evaluating-ai-systems-in-depth:")  # => co-12: states what these triggers gate
    for trigger in TRIGGERS:  # => co-12: one printed line per trigger, with its live status
        print(f"  [{'MET' if trigger.met else 'not yet'}] {trigger.condition}")  # => co-12: prints the trigger and its status
    met_triggers = [t for t in TRIGGERS if t.met]  # => co-12: which triggers this project has actually hit
    print(f"Triggers met: {len(met_triggers)}/{len(TRIGGERS)}")  # => co-12: prints the count met
    assert len(met_triggers) == 2, "exactly two of the three triggers are met in this scenario"  # => co-12: confirms the fixture
    assert len(met_triggers) >= 1, "at least one met trigger means this project should graduate now"  # => co-12
    print("MATCH: this project has already hit two concrete triggers -- it is ready for the deep course")  # => co-12
    # => co-12: 'we might need more evals someday' is not a trigger -- a NAMED, MET condition like these is
