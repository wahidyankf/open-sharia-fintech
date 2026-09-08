---
description: The checklist of conditions that make a grill question valid or invalid.
when_to_use: Use as a final checklist before sending any grilling question to the user.
---

# Validation

A grill question is valid when ALL of the following hold:

- [ ] It presents exactly 2-4 concrete options
- [ ] Each option has a trade-off description (even a brief one)
- [ ] One option is marked **(Recommended)**
- [ ] The question addresses exactly one decision
- [ ] Options are grounded in codebase reality (not invented)
- [ ] An interactive multiple-choice tool is used when the coding agent supports it
- [ ] A free-form blank-state "type your own answer" option is surfaced explicitly (never
      implicit-only)
- [ ] A "chat about this" option is offered

A grill question is invalid when ANY of the following hold:

- No options are presented (open-ended)
- Only one option is presented (not a real choice)
- More than four substantive options are presented (too many; simplify)
- Options are not grounded in codebase reality
- Multiple decisions are bundled into one question
- The blank-state "type your own answer" option is missing or only implicit
- No "chat about this" option is offered
