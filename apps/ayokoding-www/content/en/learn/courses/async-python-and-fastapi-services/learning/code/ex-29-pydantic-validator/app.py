"""Example 29: Enforcing a Rule with a Pydantic Validator.

A field_validator runs a custom rule on a field -- a value that violates it is rejected with a 422 before the
handler runs. Run: uvicorn app:app --port 8000, then:
curl -X POST -H 'Content-Type: application/json' -d '{"email":"bad"}' localhost:8000/users  (co-12, co-13)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel, field_validator  # => field_validator is Pydantic v2's custom-rule verb (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves


class UserIn(BaseModel):  # => the request-body shape
    email: str  # => a plain string on the type level -- the validator below tightens the rule (co-13)

    @field_validator("email")  # => a custom rule that runs during validation (co-12, co-13)
    @classmethod
    def must_contain_at(cls, value: str) -> str:  # => receives the raw value, returns the validated value
        if "@" not in value:  # => the rule: an email must contain "@"
            raise ValueError("email must contain '@'")  # => a violation becomes a 422, never a 500 (co-13)
        return value  # => the accepted value, passed through to the handler


@app.post("/users", status_code=201)  # => a create route
def create_user(user: UserIn) -> UserIn:  # => validation (including the rule above) already ran before this
    return user  # => only a rule-satisfying email reaches this line (co-14)
