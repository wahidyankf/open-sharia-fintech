# pyright: strict
"""Example 14: Field-Level Validation Errors in problem+json. (co-08)

RFC 9457 lets a problem type add its OWN extension members beyond the five
required fields. A validation failure adds an `errors` list naming exactly
which fields failed and why, so a client's form can highlight them directly.
"""

from dataclasses import dataclass, field, asdict  # => field: default_factory for the list member


@dataclass  # => co-08: one specific field's own failure reason
class FieldError:  # => co-08: a single (field name, message) pair
    field: str  # => which field failed
    message: str  # => why it failed


@dataclass  # => co-08: the standard 5 fields, PLUS one extension member
class ValidationProblem:  # => co-08: RFC 9457's shape, extended with a field-error list
    type: str  # => the stable problem category URI
    title: str  # => a short, human summary of that category
    status: int  # => the HTTP status, repeated inside the body
    detail: str  # => a general explanation of the whole failure
    instance: str  # => this occurrence's own identifying URI
    errors: list[FieldError] = field(default_factory=list[FieldError])  # => the extension member


def validate_new_user(username: str, age: int) -> ValidationProblem | None:  # => None means valid
    errors: list[FieldError] = []  # => co-08: accumulate EVERY failing field, not just the first
    if not username:  # => a genuinely empty username fails
        errors.append(FieldError("username", "must not be empty"))  # => records the field failure
    if age < 0:  # => a negative age fails (same rule as Example 8's 422 case)
        errors.append(FieldError("age", "must be non-negative"))  # => records the field failure
    if not errors:  # => nothing failed -- the body is valid, no problem to report
        return None  # => co-08: a clean pass returns no problem body at all
    return ValidationProblem(  # => co-08: one problem body, carrying ALL the field errors found
        type="https://api.example.com/problems/validation-error",  # => the stable category
        title="Validation Failed",  # => a short, human summary
        status=422,  # => matches Example 8's 422 for a semantic validation failure
        detail="One or more fields failed validation.",  # => a general summary of the failure
        instance="/users",  # => the endpoint this occurrence happened against
        errors=errors,  # => the field-level list accumulated above
    )  # => end of the ValidationProblem construction


result = validate_new_user(username="", age=-3)  # => BOTH rules fail on this input
assert result is not None  # => confirms validation actually caught something
# => result.errors has 2 entries: one for "username", one for "age"
print(f"status={result.status}, errors={[asdict(e) for e in result.errors]}")  # => Output: BOTH listed

ok = validate_new_user(username="grace", age=37)  # => a fully valid input
print(f"valid input result: {ok}")  # => Output: None -- no problem body needed
