"""Stdlib unittest suite for greetkit -- the capstone's :terminal check."""

import unittest

from greetkit import build_message, shout_message


class GreetkitTests(unittest.TestCase):
    def test_build_message_with_name(self):
        self.assertEqual(build_message("Neovim"), "Hello, Neovim!")

    def test_build_message_default(self):
        self.assertEqual(build_message(""), "Hello, World!")

    def test_shout_message(self):
        self.assertEqual(shout_message("Neovim"), "HELLO, NEOVIM!")


if __name__ == "__main__":
    unittest.main()
