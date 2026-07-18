# learning/code/ex-51-spec-driven-tdd-agent-session/spec.md

# Spec: Shipping Fee Calculator

## Acceptance criteria

- AC1. Orders with subtotal >= $50.00 ship free (fee = 0.00).
- AC2. Orders with subtotal < $50.00 pay a flat $5.00 fee.
- AC3. An express flag adds a $10.00 surcharge on top of AC1/AC2's result.
- AC4. The fee is always a non-negative float, rounded to 2 decimal places.
