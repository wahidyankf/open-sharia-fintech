"""Example 12: pytest verification for `with lock:` vs Manual acquire()/release()."""

import threading

from example import context_manager_releases_on_exception, context_manager_style, manual_style


def test_both_styles_execute_the_critical_section() -> None:
    log: list[str] = []
    manual_style(threading.Lock(), log)
    context_manager_style(threading.Lock(), log)
    assert log == ["manual-inside", "with-inside"]


def test_with_statement_releases_the_lock_on_exception() -> None:
    still_locked = context_manager_releases_on_exception(threading.Lock())
    assert still_locked is False  # => `with` guarantees release even when the body raises


# => Run: pytest -- Output: 2 passed
