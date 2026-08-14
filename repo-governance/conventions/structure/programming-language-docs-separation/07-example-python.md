---
title: "Example 2: Python — Correct Separation"
description: A worked example contrasting an ayokoding-www generic exception-handling lesson with the corresponding docs/explanation/ OSE Platform domain exception hierarchy
when_to_use: Read this when you need a concrete Python-based illustration of how educational and repository-specific content should be split.
category: explanation
subcategory: conventions
tags:
  - documentation
  - programming-languages
  - style-guides
  - content-separation
  - dry-principle
created: 2026-02-04
---

# Example 2: Python - Correct Separation

**ayokoding-www** (`apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/python/in-practice/error-handling.md`):

````markdown
# Error Handling in Python

Generic Python error patterns.

## Exception Handling

Python uses try/except for error handling:

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Invalid value: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    cleanup()
```
````

Key takeaway: Use specific exception types, always handle errors explicitly.

````

**docs/explanation/** (`docs/explanation/software-engineering/programming-languages/python/error-handling.md`):

```markdown
# Python Error Handling - OSE Platform Standards

**Prerequisite**: Complete [ayokoding-www Python Error Handling](https://ayokoding.com/en/learn/software-engineering/programming-languages/python/in-practice/error-handling/).

## OSE Platform Exception Hierarchy

OSE Platform defines a domain exception hierarchy for Shariah compliance:

```python
# Domain exceptions
class ShariaComplianceError(Exception):
    """Base exception for Shariah violations"""
    pass

class InterestViolationError(ShariaComplianceError):
    """Raised when interest (riba) is detected"""
    def __init__(self, amount: Decimal, transaction_id: str):
        self.amount = amount
        self.transaction_id = transaction_id
        super().__init__(f"Interest detected: {amount} in {transaction_id}")

class ProhibitedInvestmentError(ShariaComplianceError):
    """Raised when investment violates Shariah"""
    pass
````

**Usage in services**:

```python
def validate_transaction(transaction: Transaction) -> None:
    if transaction.interest_amount > 0:
        raise InterestViolationError(
            amount=transaction.interest_amount,
            transaction_id=transaction.id
        )
```

**Why**: Domain exceptions enable Shariah audit trails, compliance monitoring, clear error semantics.

```

**Why this works**:

- **Separation**: ayokoding-www teaches Python exceptions (generic), docs/explanation/ defines OSE Platform domain exceptions
- **Prerequisite**: docs/explanation/ explicitly links to ayokoding-www
- **No duplication**: Generic try/except in ayokoding-www, domain hierarchy in docs/explanation/
- **Clear scope**: ayokoding-www = Python fundamentals, docs/explanation/ = Shariah compliance patterns
```
