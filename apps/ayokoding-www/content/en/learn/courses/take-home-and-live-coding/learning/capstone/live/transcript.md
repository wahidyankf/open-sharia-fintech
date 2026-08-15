# Live round transcript — fictional ticket list

This is a rehearsal transcript, not a claim about any company’s editor or rubric. The candidate uses a local terminal and the small Python files in `code/`; every checkpoint is intentionally runnable.

| Checkpoint             | Narration and collaboration move                                                                                                                                                                                                    | Observable evidence                                                     |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 0 · clarify            | **Candidate:** “Should a ticket contain only a title? What should happen for blank titles, and is output order part of the requirement?” **Interviewer:** “Titles only; reject blank input. Deterministic display would be useful.” | Constraints are asked before the interface is chosen.                   |
| 1 · green minimum      | **Candidate:** “I will first return an empty list so we have an executable baseline, then add one validated operation.” Runs `pytest -q`.                                                                                           | `first_checkpoint()` test passes.                                       |
| 2 · narrate state      | **Candidate:** “A list is enough because the brief asks only to collect titles; I will return a new list so callers retain their previous state.”                                                                                   | `add_ticket` appends one cleaned title without mutation.                |
| 3 · take the steer     | **Interviewer:** “Could results be predictable for a reviewer?” **Candidate:** “Yes. I will add a separate presentation function instead of sorting storage.”                                                                       | `visible_titles` is a small, case-insensitive sort and its test passes. |
| 4 · reproduce a defect | **Candidate:** “I suspect whitespace-only input would look present until display. I will make that a focused failing expectation first.”                                                                                            | The blank-title assertion names the suspected boundary.                 |
| 5 · repair and close   | **Candidate:** “The boundary belongs in `add_ticket`; the error tells the caller what to fix. I will rerun all focused tests now. The remaining trade-off is that this has no IDs or persistence because neither is in the brief.”  | `pytest -q` is green; the deferral is explicit.                         |

## Self-review prompts

1. Did you ask each requirement question before writing an assumption into code?
2. Could a partner identify the state, invariant, and reason for each edit from your narration?
3. Did every checkpoint execute before the next extension?
4. Did the response to the hint acknowledge the partner and make the change easier to inspect?
5. When uncertain, did you name the evidence you would seek rather than bluff?
