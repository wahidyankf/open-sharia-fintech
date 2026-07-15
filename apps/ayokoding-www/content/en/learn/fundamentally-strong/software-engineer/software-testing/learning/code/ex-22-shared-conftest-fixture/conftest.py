import pytest  # => conftest.py is pytest's AUTO-DISCOVERED, no-import-needed fixture home (co-09)


@pytest.fixture
def shared_greeting() -> str:  # => defined ONCE here, usable by EVERY test file in this directory  # fmt: skip
    return "hello from conftest"  # => a plain string -- the content itself is not the point here  # fmt: skip
    # => neither test_example.py nor test_more.py IMPORTS this fixture explicitly --
    # => pytest finds conftest.py automatically and makes its fixtures available by name
