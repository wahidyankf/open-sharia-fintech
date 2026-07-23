from pipeline import (
    compute_total,
)  # => co-01/co-23: the SAME function this capstone's regression tests guard, both cases


def test_compute_total_with_discount():  # => co-23: the ORIGINAL passing case -- must stay green through BOTH fixes
    assert (
        compute_total({"price": 10.0, "qty": 2, "discount": 3.0}) == 17.0
    )  # => co-23: 10*2 - 3 = 17.0, unaffected by either fix


def test_compute_total_without_discount():  # => co-01/co-23: the REGRESSION test -- red before the fix, green after
    assert (
        compute_total({"price": 10.0, "qty": 2}) == 20.0
    )  # => co-01: no "discount" key -- would KeyError before the fix, .get()s to 0.0 after
