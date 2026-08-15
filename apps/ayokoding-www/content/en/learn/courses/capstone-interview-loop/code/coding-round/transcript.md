# Timed coding round transcript

Work under a 42-minute total timer. Fill the evidence before reviewing the reference implementation.

## Prompt 1 · Pair indices (hash lookup, 20 minutes)

- **Clarify:** Is exactly one pair expected? May a value be reused? What should no pair return?
- **Concrete trace:** `[2, 7, 11, 15]`, target `9`: store `2 → 0`; at `7`, complement `2` is stored;
  return `(0, 1)`.
- **Plan and invariant:** Scan once, mapping each earlier value to its index. Before inspecting index
  `i`, `seen` contains precisely the values from indices below `i`, so a stored complement gives a
  valid earlier partner.
- **Complexity:** `O(n)` time and `O(n)` extra space.
- **Verify:** Run `pytest -q code/coding-round`; explain the duplicate and no-pair cases aloud.
- **Self-score (1–4):** correctness [ ], communication [ ], complexity [ ], edge cases [ ].

## Prompt 2 · Compact window (sliding window, 20 minutes)

- **Clarify:** Is the unit a character? Is an empty string valid? Do we need the substring or its
  length?
- **Concrete trace:** `abcabcbb`: advance right; on the second `a`, move the left edge after the
  previous `a`; the longest observed width remains `3`.
- **Plan and invariant:** Keep a window with no repeated character and a map of each character's most
  recent index. A repeated character inside the current window moves the left edge forward only.
- **Complexity:** `O(n)` time and `O(min(n, alphabet))` extra space.
- **Verify:** Run `pytest -q code/coding-round`; explain the empty and repeated-character cases aloud.
- **Self-score (1–4):** correctness [ ], communication [ ], complexity [ ], edge cases [ ].

## Close (2 minutes)

State the chosen pattern and trade-off for each solve, then record one repair for any rating below 4.
