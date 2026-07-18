# learning/code/ex-38-gherkin-driven-implementation/step_runner.py
"""Example 38: A Gherkin Scenario Driving a Small Step-Style Implementation."""  # => co-21: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import pathlib  # => co-21: locates shopping_cart.feature next to this file -- no hardcoded absolute path
import re  # => co-21: extracts the numeric literals embedded in each Gherkin step's plain-English sentence
from typing import cast  # => co-21: narrows STATE's necessarily-untyped dict[str, object] values back to their real shape


def calculate_total(prices: list[float]) -> float:  # => co-21: the implementation the agent writes TO SATISFY the spec below
    """Discount engine under test: 10% off once the cart subtotal exceeds $100."""  # => co-21: documents calculate_total's contract -- no runtime output, just sets its __doc__
    subtotal = sum(prices)  # => co-21: the raw sum, before any discount is applied
    if subtotal > 100:  # => co-21: the ONE business rule this spec's scenario exercises
        return round(subtotal * 0.9, 2)  # => co-21: 10% off, rounded to cents
    return round(subtotal, 2)  # => co-21: no discount below the threshold


STATE: dict[str, object] = {}  # => co-21: carries data between Given/When/Then steps, exactly as a real BDD runner would


def step_given_cart(line: str) -> None:  # => co-21: matches: Given a cart containing items priced at ...
    """Matches: Given a cart containing items priced at ..."""  # => co-21: documents step_given_cart's contract -- no runtime output, just sets its __doc__
    STATE["prices"] = [float(x) for x in re.findall(r"\d+\.\d+", line)]  # => co-21: pulls every decimal price out of the step's plain-English text


def step_when_calculate(line: str) -> None:  # => co-21: matches: When the discount engine calculates the final total
    """Matches: When the discount engine calculates the final total"""  # => co-21: documents step_when_calculate's contract -- no runtime output, just sets its __doc__
    prices = cast(list[float], STATE["prices"])  # => co-21: STATE's values are typed object -- narrow back to list[float] here
    STATE["result"] = calculate_total(prices)  # => co-21: runs the implementation under test against the Given step's prices


def step_then_total(line: str) -> None:  # => co-21: matches: Then the final total should be ...
    """Matches: Then the final total should be ..."""  # => co-21: documents step_then_total's contract -- no runtime output, just sets its __doc__
    expected = float(re.findall(r"\d+\.\d+", line)[0])  # => co-21: the scenario's own literal acceptance number, read straight from the .feature file
    actual = STATE["result"]  # => co-21: what the implementation actually computed in the When step
    assert actual == expected, f"expected {expected}, got {actual}"  # => co-21: THIS is the scenario passing or failing -- the whole point of this file


STEP_TABLE = [  # => co-21: maps each Gherkin step PREFIX to the step function that implements it
    (re.compile(r"^Given a cart"), step_given_cart),  # => co-21: routes any "Given a cart..." line to step_given_cart
    (re.compile(r"^When the discount engine"), step_when_calculate),  # => co-21: routes any matching "When..." line to step_when_calculate
    (re.compile(r"^Then the final total"), step_then_total),  # => co-21: routes any matching "Then..." line to step_then_total
]  # => co-21: closes the multi-line construct opened above


def run_feature_file(path: pathlib.Path) -> list[str]:  # => co-21: a tiny, standard-library-only Gherkin step runner
    """Parse a .feature file's Given/When/Then steps and execute each against STEP_TABLE."""  # => co-21: documents run_feature_file's contract -- no runtime output, just sets its __doc__
    executed: list[str] = []  # => co-21: records every step actually executed, in order
    for raw_line in path.read_text().splitlines():  # => co-21: reads the REAL .feature file colocated with this script
        line = raw_line.strip()  # => co-21: Gherkin steps are indented -- strip before matching
        if not line.startswith(("Given", "When", "Then")):  # => co-21: skips the Feature/Scenario headers and blank lines
            continue  # => co-21: only Given/When/Then lines drive the implementation
        for pattern, step_fn in STEP_TABLE:  # => co-21: finds the FIRST step definition whose pattern matches this line
            if pattern.match(line):  # => co-21: a real step-matching dispatch, not a hardcoded index
                step_fn(line)  # => co-21: executes the matched step against the CURRENT step's exact text
                executed.append(line)  # => co-21: records this step as having run
                break  # => co-21: stops searching once a match is found -- the first match wins
        else:  # => co-21: a for/else -- runs ONLY if no `break` fired, i.e. no step definition matched
            raise LookupError(f"no step definition matches: {line!r}")  # => co-21: fails loudly instead of silently skipping an unimplemented step
    return executed  # => co-21: the full, ordered list of steps this scenario actually ran


if __name__ == "__main__":  # => co-21: entry point -- this block runs only when the file executes directly, not on import
    feature_path = pathlib.Path(__file__).parent / "shopping_cart.feature"  # => co-21: resolved relative to THIS file, never an absolute path
    executed_steps = run_feature_file(feature_path)  # => co-21: parses and runs the real .feature file's scenario
    for step in executed_steps:  # => co-21: prints each step as it passed
        print(f"PASS: {step}")  # => co-21: a step only appears here if its step function did NOT raise
    assert len(executed_steps) == 3, "all three Given/When/Then steps must execute"  # => co-21: proves the whole scenario ran, not a subset
    print("\nScenario 'Cart subtotal over $100 gets a 10% discount' passed: True")  # => co-21: this file is self-verifying -- a clean exit proves the scenario passed
