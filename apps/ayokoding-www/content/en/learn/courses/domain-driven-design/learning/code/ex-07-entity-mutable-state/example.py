# => Keeps this domain step explicit and reviewable.
"""Example 7: an entity can change while preserving identity."""


# => Gives domain rules a single, named home.
class Customer:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, id: str, email: str) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.id, self.email = (
            # => Keeps this domain step explicit and reviewable.
            id,
            # => Keeps this domain step explicit and reviewable.
            email,
        )  # => identity and mutable contact detail are separate

    # => Names policy so callers do not recreate the rule.
    def change_email(self, email: str) -> None:
        self.email = email  # => a named state transition retains the id


customer = Customer("c-1", "old@example.test")  # => capture stable identity
customer.change_email("new@example.test")  # => only the mutable attribute changes
assert customer.id == "c-1" and customer.email.startswith("new")  # => continuity holds
print(customer.id)  # => Output: c-1
