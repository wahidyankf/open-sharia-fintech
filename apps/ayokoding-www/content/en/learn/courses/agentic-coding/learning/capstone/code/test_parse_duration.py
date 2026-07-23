from parse_duration import parse_duration
import pytest


def test_hours_and_minutes():
    assert parse_duration("1h30m") == 5400


def test_seconds_only():
    assert parse_duration("45s") == 45


def test_all_three_units():
    assert parse_duration("1h1m1s") == 3661


def test_zero_valued_token():
    assert parse_duration("0h") == 0


def test_empty_string_rejected():
    with pytest.raises(ValueError):
        parse_duration("")


def test_garbage_suffix_rejected():
    with pytest.raises(ValueError):
        parse_duration("1h30mx")


def test_no_tokens_rejected():
    with pytest.raises(ValueError):
        parse_duration("hello")
