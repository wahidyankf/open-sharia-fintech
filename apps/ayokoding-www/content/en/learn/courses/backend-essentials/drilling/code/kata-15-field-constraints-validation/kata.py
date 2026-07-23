def validate_constraints(body: dict[str, object]) -> list[str]:  # => co-10: mimics Pydantic-style field rules
    errors: list[str] = []  # => co-11: collect ALL violations, not just the first -- one 422 lists them all
    title = body.get("title")
    if not isinstance(title, str) or len(title) < 3:  # => co-10: min_length=3 equivalent
        errors.append("title: must be a string with min_length 3")
    quantity = body.get("quantity")
    if not isinstance(quantity, int) or quantity <= 0:  # => co-10: gt=0 equivalent
        errors.append("quantity: must be an integer greater than 0")
    return errors  # => empty list means the body satisfies every constraint


valid_body: dict[str, object] = {"title": "Ship it", "quantity": 3}
short_title_body: dict[str, object] = {"title": "Hi", "quantity": 3}  # => violates min_length
bad_quantity_body: dict[str, object] = {"title": "Ship it", "quantity": 0}  # => violates gt=0
both_bad_body: dict[str, object] = {"title": "Hi", "quantity": -1}  # => violates BOTH constraints

print(validate_constraints(valid_body))  # => Output: []
print(validate_constraints(short_title_body))  # => Output: ['title: must be a string with min_length 3']
print(validate_constraints(bad_quantity_body))  # => Output: ['quantity: must be an integer greater than 0']
print(validate_constraints(both_bad_body))  # => Output: ['title: must be a string with min_length 3', 'quantity: must be an integer greater than 0']

assert validate_constraints(valid_body) == []  # => co-10: nothing to reject -- the body is valid
assert len(validate_constraints(short_title_body)) == 1
assert len(validate_constraints(both_bad_body)) == 2  # => co-11: BOTH violations reported in one 422, not just the first
print("kata-15 OK")
