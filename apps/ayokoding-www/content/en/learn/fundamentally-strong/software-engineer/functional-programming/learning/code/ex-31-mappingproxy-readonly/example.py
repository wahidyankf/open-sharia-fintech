"""Example 31: A Read-Only View via MappingProxyType."""

from types import (
    MappingProxyType,
)  # => a read-only VIEW over an existing dict, not a copy

config = {
    "retries": 3,
    "timeout": 5,
}  # => the underlying mutable dict this example protects
readonly_config = MappingProxyType(
    config
)  # => wraps config -- reads pass through, writes are blocked
# => this is the co-04 "immutability at the boundary" pattern -- share config without risking mutation

print(
    readonly_config["retries"]
)  # => Output: 3 -- reads work exactly like a normal dict

try:  # => opens a block that expects the write below to raise
    readonly_config["retries"] = 99  # type: ignore[index]  # => attempts a write through the view
    raised = False  # => unreachable if TypeError fires
except TypeError:  # => MappingProxyType has no __setitem__
    raised = True  # => confirms the view actually blocked the write

print(raised)  # => Output: True
config["retries"] = 10  # => the UNDERLYING dict itself is still mutable directly
print(
    readonly_config["retries"]
)  # => Output: 10 -- the view reflects the underlying dict LIVE
