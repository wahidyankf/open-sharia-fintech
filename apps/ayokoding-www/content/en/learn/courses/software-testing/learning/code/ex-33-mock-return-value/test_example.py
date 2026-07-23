# learning/code/ex-33-mock-return-value/test_example.py
"""Example 33: Configuring a Mock's Return Value."""

from unittest.mock import MagicMock  # => same mock object, this time CONFIGURED to return a value (co-13, co-12)  # fmt: skip


def get_user_display_name(user_repo, user_id: int) -> str:  # => the unit under test  # fmt: skip
    user = user_repo.get(user_id)  # => depends entirely on what user_repo.get() hands back  # fmt: skip
    return user["name"]  # => extracts one field from whatever dict was returned


def test_mock_return_value_feeds_the_unit_under_test() -> None:
    mock_repo = MagicMock()  # => arrange: a bare mock -- .get() would otherwise return ANOTHER MagicMock  # fmt: skip
    mock_repo.get.return_value = {"name": "Ada"}  # => co-13: explicitly CONFIGURES what .get() hands back  # fmt: skip
    # => without this line, user["name"] would raise TypeError -- a MagicMock is not subscriptable
    # => by default, which is why return_value must be set to a REAL dict for this test to run
    display_name = get_user_display_name(mock_repo, user_id=1)  # => act: user_id is irrelevant to the mock  # fmt: skip
    assert display_name == "Ada"  # => confirms the unit correctly consumed the CONFIGURED return value  # fmt: skip
