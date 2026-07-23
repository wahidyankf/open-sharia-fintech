# ex-22b: a COMPLETELY SEPARATE test file, reusing the SAME conftest.py fixture (co-09)
def test_second_file_also_sees_it(shared_greeting: str) -> None:
    # => this file never imports test_example.py OR conftest.py directly -- the fixture
    # => is shared purely because both files live in the same directory as conftest.py
    assert len(shared_greeting) > 0  # => a second, independent assertion on the same shared value  # fmt: skip
    assert "conftest" in shared_greeting  # => confirms it's genuinely the SAME string both files see  # fmt: skip
