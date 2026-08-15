# Narrated live round transcript

Set a 25-minute timer and run `pytest -q code/live` after every checkpoint. Speak these actions aloud
while performing them; replace the blank observations with what actually happened.

1. **Clarify (0–3 min):** “The smallest useful behavior is an ordered list of named checkpoints. Is an
   empty name invalid?” Record the answer: \_\_.
2. **Narrow slice (3–10 min):** Add `add_checkpoint` by copying the existing list into a new list.
   Narrate why preserving the caller's list is part of the contract. Test result: \_\_.
3. **Edge case (10–16 min):** Reject blank checkpoint names with an actionable error. Explain the
   validation before implementing it. Test result: \_\_.
4. **Review (16–22 min):** Read the function and tests aloud, name one trade-off (small in-memory
   list, no persistence), and ask whether that scope is sufficient. Response: \_\_.
5. **Close (22–25 min):** Run the focused suite again, state what remains out of scope, and write the
   next smallest increment rather than extending the exercise silently. Final result: \_\_.
