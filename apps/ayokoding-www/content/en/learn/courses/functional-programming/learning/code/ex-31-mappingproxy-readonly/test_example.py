"""Example 31: pytest verification for A Read-Only View via MappingProxyType."""

from types import MappingProxyType


def test_view_blocks_writes_but_reflects_the_underlying_dict() -> None:
    config = {"retries": 3}
    readonly_config = MappingProxyType(config)
    try:
        readonly_config["retries"] = 99  # type: ignore[index]
        raised = False
    except TypeError:
        raised = True
    assert raised is True

    config["retries"] = 10  # => mutate the underlying dict directly
    assert readonly_config["retries"] == 10  # => the view is LIVE, not a snapshot


# => Run: pytest -- Output: 1 passed
