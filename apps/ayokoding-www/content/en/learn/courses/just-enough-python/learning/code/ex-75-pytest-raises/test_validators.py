"""Example 75: pytest.raises around require_positive."""

import pytest  # => imports the pytest testing framework

from validators import require_positive  # => imports the function under test


# pytest discovers this test via its test_ prefix.
def test_require_positive_rejects_zero() -> None:
    with pytest.raises(ValueError):  # => passes ONLY if the block raises ValueError
        require_positive(0)  # => the call expected to raise


# => Run: pytest -- Output: 1 passed
