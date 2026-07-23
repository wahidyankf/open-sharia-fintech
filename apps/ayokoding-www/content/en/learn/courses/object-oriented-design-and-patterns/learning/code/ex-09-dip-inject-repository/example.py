"""Example 9: Invert a Service to Depend on a Repository Protocol."""  # => module docstring

from typing import Protocol  # => Protocol declares the abstraction UserService depends on


class Repository(Protocol):  # => the ABSTRACTION -- high-level policy owns this shape
    # => both the high-level UserService AND the low-level detail depend on THIS
    def get(self, user_id: int) -> str:  # => the one method any repository must provide
        ...  # => Protocol methods have no body -- a structural contract only


class InMemoryRepository:  # => a concrete LOW-level detail -- one of many possible ones
    def __init__(self) -> None:  # => the constructor
        self._data: dict[int, str] = {1: "Alice", 2: "Bob"}  # => sample in-memory data

    def get(self, user_id: int) -> str:  # => satisfies Repository structurally
        return self._data[user_id]  # => a real, honest implementation


class UserService:  # => the HIGH-level policy -- depends on the abstraction, not detail
    def __init__(  # => the constructor, spread across lines to annotate each parameter
        self,  # => the UserService instance being constructed
        repository: Repository,
        # => the constructor names the PROTOCOL, never a concrete repository class
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.repository = repository  # => held as a collaborator, injected from outside

    def greet(self, user_id: int) -> str:  # => defines the greet() method
        name: str = self.repository.get(
            user_id  # => any Repository-shaped object answers this the same way
        )  # => the DIRECTION of dependency: UserService -> Repository, never reversed
        return f"Hi, {name}"  # => builds the greeting from injected data


service: UserService = UserService(
    InMemoryRepository()  # => a MySQLRepository could be swapped in with this one line
)  # => the concrete detail is chosen HERE, at construction time, not inside UserService
print(service.greet(1))  # => confirms the injected repository actually supplied the data
# => Output: Hi, Alice
# => `UserService.__init__` never imports or names `InMemoryRepository` -- only `Repository`
# => swapping storage engines never touches a single line inside UserService
