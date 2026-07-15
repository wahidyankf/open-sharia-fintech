# learning/code/ex-40-fake-vs-mock-contrast/test_example.py
"""Example 40: Fake vs. Mock -- Two Ways to Check the Same Thing."""

from unittest.mock import MagicMock  # => the MOCK half of this contrast -- checks INTERACTION, not state (co-13)  # fmt: skip


class InMemoryUserRepo:  # => the SAME fake as ex-39 -- genuinely stores and retrieves (co-16)  # fmt: skip
    def __init__(self) -> None:  # => same constructor shape as ex-39's fake  # fmt: skip
        self._users: dict[int, str] = {}  # => real in-memory storage

    def save(self, user_id: int, name: str) -> None:  # => a real method, genuinely mutates state  # fmt: skip
        self._users[user_id] = name  # => a REAL write


class UserService:  # => the SAME unit under test as ex-39 -- unaware which kind of repo it holds  # fmt: skip
    def __init__(self, repo) -> None:  # => still no type hint -- fake or mock, either satisfies this  # fmt: skip
        self.repo = repo

    def register(self, user_id: int, name: str) -> None:  # => the ONE method both tests below exercise  # fmt: skip
        self.repo.save(user_id, name)  # => delegates to repo.save -- fake writes for real, mock just records  # fmt: skip


def test_fake_asserts_on_resulting_STATE() -> None:  # => the FAKE half: checks WHAT ENDED UP TRUE  # fmt: skip
    fake_repo = InMemoryUserRepo()  # => arrange: a real, working (if lightweight) implementation  # fmt: skip
    service = UserService(fake_repo)  # => act setup
    service.register(1, "Ada")  # => act: a genuine write into the fake's own dict
    assert fake_repo._users == {1: "Ada"}  # => assert on STATE: what does the repo now CONTAIN? (co-16)  # fmt: skip


def test_mock_asserts_on_the_recorded_INTERACTION() -> None:  # => the MOCK half: checks HOW IT WAS CALLED  # fmt: skip
    mock_repo = MagicMock()  # => arrange: records calls, stores NOTHING real at all
    service = UserService(
        mock_repo
    )  # => act setup, identical UserService code as above
    service.register(1, "Ada")  # => act: this time, no real dict is ever written to
    mock_repo.save.assert_called_once_with(1, "Ada")  # => assert on INTERACTION: was save() called correctly? (co-13)  # fmt: skip
    # => both tests exercise the IDENTICAL UserService.register call -- what differs is
    # => WHAT is being verified: the fake's test checks the resulting state (classical/Beck-style
    # => testing); the mock's test checks the interaction itself (mockist/London-style testing)
