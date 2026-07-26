# learning/code/ex-42-eval-before-adding-retrieval/before_retrieval.py
"""Worked Example 42: Eval Before Adding Retrieval."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

FIXED_CASES = {"case-05": "5 GB", "case-06": "50 GB", "case-11": "Pro"}  # => co-03: the SAME three cases, before and after
NO_RETRIEVAL_ANSWERS = {  # => co-01: the system answering from the model's own memory alone -- no lookup step
    "case-05": "The Free plan accepts fairly large files.",  # => co-01: vague -- no exact figure
    "case-06": "The Pro plan accepts even larger files.",  # => co-01: vague -- no exact figure
    "case-11": "The REST API is available on several plans.",  # => co-01: vague -- no named plan
}  # => co-01: closes NO_RETRIEVAL_ANSWERS -- vague on every case, the model is guessing without a source to check
KNOWLEDGE_BASE = {"case-05": "5 GB", "case-06": "50 GB", "case-11": "Pro"}  # => co-09: the exact facts NO_RETRIEVAL_ANSWERS lacked


def answer_with_retrieval(case_id: str) -> str:  # => co-09: the SAME system, now with a retrieval step added
    """Look the exact fact up in KNOWLEDGE_BASE before answering, instead of guessing from memory."""  # => co-09: documents answer_with_retrieval's contract -- no runtime output, just sets its __doc__
    fact = KNOWLEDGE_BASE[case_id]  # => co-09: the retrieval step -- an exact fact, not a guess
    return f"According to the current docs, the answer is {fact}."  # => co-09: the fact, stated exactly


def run_eval(answers: dict[str, str]) -> float:  # => co-09: the SAME eval logic, run both before and after retrieval
    """Return the substring-scored pass rate of `answers` against FIXED_CASES."""  # => co-09: documents run_eval's contract -- no runtime output, just sets its __doc__
    verdicts = [FIXED_CASES[cid] in answers[cid] for cid in FIXED_CASES]  # => co-05: substring scoring, unchanged
    return sum(verdicts) / len(verdicts)  # => co-07: reduce to the headline pass rate


if __name__ == "__main__":  # => co-09: entry point -- runs only when this file executes directly, not on import
    before_rate = run_eval(NO_RETRIEVAL_ANSWERS)  # => co-09: "run the gate" -- BEFORE retrieval is added
    print(f"Before retrieval: {before_rate:.0%}")  # => co-07: prints the pre-retrieval headline number
    after_answers = {cid: answer_with_retrieval(cid) for cid in FIXED_CASES}  # => co-09: "add retrieval" -- the ONLY change made
    after_rate = run_eval(after_answers)  # => co-09: "rerun" -- the SAME eval, the SAME fixed cases
    print(f"After retrieval: {after_rate:.0%}")  # => co-07: prints the post-retrieval headline number
    delta = after_rate - before_rate  # => co-09: the exact, attributable improvement
    print(f"Delta attributable to retrieval: {delta:+.0%}")  # => co-09: prints the isolated effect of the ONE change made
    assert before_rate == 0.0, "without retrieval, this fixture's vague answers must fail every case"  # => co-09
    assert after_rate == 1.0, "with retrieval, this fixture's exact answers must pass every case"  # => co-09
    print("MATCH: because nothing else changed, the entire delta is attributable to adding retrieval")  # => co-09
    # => co-09: measure the gate BEFORE a structural change (retrieval, agents) to isolate what that ONE change actually did
