import tempfile
import unittest
from pathlib import Path

from store import move_branch, read_blob, write_blob


class StoreTests(unittest.TestCase):
    def test_round_trip_and_ref_are_isolated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            identifier = write_blob(root, b"hello")
            move_branch(root, "main", identifier)
            self.assertEqual(b"hello", read_blob(root, identifier))
            self.assertEqual(
                identifier + "\n", (root / "refs" / "heads" / "main").read_text()
            )


if __name__ == "__main__":
    unittest.main()
