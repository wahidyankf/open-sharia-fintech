"""Tests for the idempotent projection drilling kata."""

import unittest

from kata import apply_once


class KataTests(unittest.TestCase):
    def test_duplicate_has_no_second_effect(self) -> None:
        seen: set[str] = set()
        projection: dict[str, str] = {}
        self.assertTrue(apply_once(seen, projection, "m-1", "o-1", "paid"))
        self.assertFalse(apply_once(seen, projection, "m-1", "o-1", "paid"))
        self.assertEqual(projection, {"o-1": "paid"})


if __name__ == "__main__":
    unittest.main()
