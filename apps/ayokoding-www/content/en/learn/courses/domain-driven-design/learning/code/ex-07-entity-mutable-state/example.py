"""Example 7: an entity can change while preserving identity."""


class Customer:
    def __init__(self, id: str, email: str) -> None:
        self.id, self.email = (
            id,
            email,
        )  # => identity and mutable contact detail are separate

    def change_email(self, email: str) -> None:
        self.email = email  # => a named state transition retains the id


customer = Customer("c-1", "old@example.test")  # => capture stable identity
customer.change_email("new@example.test")  # => only the mutable attribute changes
assert customer.id == "c-1" and customer.email.startswith("new")  # => continuity holds
print(customer.id)  # => Output: c-1
