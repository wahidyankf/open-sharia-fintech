# learning/code/ex-02-same-input-two-answers/two_calls.py
"""Worked Example 2: Same Input, Two Answers."""  # => co-08: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import random  # => co-08: stands in for the model's own internal sampling randomness

QUESTION = "How much free storage does Nimbus give a new account?"  # => co-08: the exact same input, called twice
KEY_FACT = "15 GB"  # => co-08: the fact a correct answer must contain, regardless of phrasing


def mock_model_call(question: str, *, seed: int) -> str:  # => co-08: stands in for a real, non-deterministic model call
    """Return one of three phrasings, chosen by `seed` -- a mocked stand-in for sampling temperature."""  # => co-08: documents mock_model_call's contract -- no runtime output, just sets its __doc__
    del question  # => co-08: unused in this mock -- every phrasing answers the one fixed QUESTION
    rng = random.Random(seed)  # => co-08: a seeded generator -- deterministic PER seed, varying ACROSS seeds
    phrasings = [  # => co-08: three outputs a real model might plausibly sample for the same prompt
        "New Nimbus accounts start with 15 GB of free storage.",  # => co-08: phrasing 1 -- keeps the key fact
        "Nimbus gives you 15 GB free right out of the box.",  # => co-08: phrasing 2 -- keeps the key fact, different wording
        "You get a generous amount of free storage to start.",  # => co-08: phrasing 3 -- DROPS the key fact entirely
    ]  # => co-08: closes the phrasings list
    return rng.choice(phrasings)  # => co-08: the "sample" -- which entry depends only on the seed


if __name__ == "__main__":  # => co-08: entry point -- runs only when this file executes directly, not on import
    call_1 = mock_model_call(QUESTION, seed=1)  # => co-08: "call 1" -- the same prompt, seed standing in for call-to-call variance
    call_2 = mock_model_call(QUESTION, seed=5)  # => co-08: "call 2" -- identical prompt, different sampled outcome
    print(f"Call 1 -> {call_1!r}")  # => co-08: prints the first sampled answer
    print(f"Call 2 -> {call_2!r}")  # => co-08: prints the second sampled answer
    outputs_differ = call_1 != call_2  # => co-08: the defining symptom of a stochastic system
    print(f"Outputs differ: {outputs_differ}")  # => co-08: True -- same input, two distinct answers
    assert outputs_differ, "two calls on the identical input must differ for this demo to make its point"  # => co-08
    call_1_ok = KEY_FACT in call_1  # => co-08: does call 1 keep the fact that actually matters?
    call_2_ok = KEY_FACT in call_2  # => co-08: does call 2 keep the same fact?
    print(f"Call 1 keeps {KEY_FACT!r}: {call_1_ok} | Call 2 keeps {KEY_FACT!r}: {call_2_ok}")  # => co-08
    assert call_1_ok and not call_2_ok, "one call must keep the fact and the other must drop it"  # => co-08: the risk this poses
    # => co-08: a single run's pass/fail is not yet evidence -- re-running is the cheapest reliability check there is
