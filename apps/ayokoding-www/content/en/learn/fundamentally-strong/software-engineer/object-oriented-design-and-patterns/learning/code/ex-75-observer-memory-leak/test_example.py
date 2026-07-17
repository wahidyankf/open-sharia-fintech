"""Example 75: pytest verification that weakref fixes the observer memory leak."""

import gc

from example import Event, LeakySubject, WeakRefSubject


def test_leaky_subject_keeps_an_unsubscribed_observer_alive() -> None:
    subject = LeakySubject()
    observer = Event("leak-me")
    subject.subscribe(observer)
    del observer  # => caller drops its reference
    gc.collect()
    assert subject.observer_count() == 1  # => LEAK: the subject's strong reference kept it alive


def test_weakref_subject_lets_an_unreferenced_observer_be_collected() -> None:
    subject = WeakRefSubject()
    observer = Event("collect-me")
    subject.subscribe(observer)
    del observer  # => no other strong reference exists anywhere
    gc.collect()
    assert subject.observer_count() == 0  # => FIXED: weakref did not keep it alive


def test_weakref_subject_keeps_a_still_referenced_observer() -> None:
    subject = WeakRefSubject()
    observer = Event("still-alive")  # => held here -- a strong reference DOES still exist
    subject.subscribe(observer)
    gc.collect()
    assert subject.observer_count() == 1  # => weakref only drops entries once ALL strong refs are gone


# => Run: pytest -q -- Output: 3 passed
