# Scoped take-home artifact

This deliberately small artifact checks whether a submission has the minimum reviewer-facing shape:
a README, a focused test, and an implementation file. It models scope discipline and clean-checkout
verification; it is not a production submission framework.

## Run from a clean checkout

```bash
python -m pytest -q
```

## Acceptance checks

- The README gives an exact command.
- The test demonstrates a happy path and a missing-basics path.
- The implementation is standard-library-only.
- Any requirement not represented here is consciously out of scope and should be recorded before work
  starts rather than guessed.
