# learning/code/ex-39-fake-in-memory-repo/test_example.py
"""Example 39: A Fake In-Memory Repository."""


# ex-39: a FAKE is a REAL, working implementation -- just too lightweight for production (co-16)
class InMemoryUserRepo:  # => a fake repository: genuinely stores and retrieves data, in a dict  # fmt: skip
    def __init__(self) -> None:  # => a real constructor, called once per fake instance  # fmt: skip
        self._users: dict[int, str] = {}  # => in-memory storage -- no database, no network at all  # fmt: skip

    def save(self, user_id: int, name: str) -> None:  # => genuinely mutates internal state  # fmt: skip
        self._users[user_id] = name  # => a REAL write -- not canned, not recorded-and-discarded  # fmt: skip

    def get(self, user_id: int) -> str | None:  # => genuinely reads back what was written  # fmt: skip
        return self._users.get(user_id)  # => returns None if never saved -- real lookup semantics  # fmt: skip


class UserService:  # => the unit under test -- depends on ANY object with .save()/.get()  # fmt: skip
    def __init__(self, repo) -> None:  # => no type hint on repo -- duck typing is the whole point here  # fmt: skip
        self.repo = repo  # => stores whichever repo it was given -- fake here, a real DB in production  # fmt: skip

    def register(
        self, user_id: int, name: str
    ) -> None:  # => a thin wrapper over repo.save
        self.repo.save(user_id, name)  # => delegates to WHATEVER repo was injected -- fake or real  # fmt: skip

    def lookup(self, user_id: int) -> str | None:  # => a thin wrapper over repo.get
        return self.repo.get(user_id)  # => same delegation for reads -- symmetric with register above  # fmt: skip


def test_service_works_against_the_fake_repo() -> None:  # => tests the service through a REAL, working fake  # fmt: skip
    repo = InMemoryUserRepo()  # => arrange: a genuinely working repo, just in-memory (co-16)  # fmt: skip
    service = UserService(repo)  # => act setup: the service has no idea this repo isn't a real database  # fmt: skip
    service.register(1, "Ada")  # => act: a REAL write happens inside the fake's dict  # fmt: skip
    assert service.lookup(1) == "Ada"  # => assert: a REAL read confirms the REAL write took effect  # fmt: skip
