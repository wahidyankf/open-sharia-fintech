"""Integration tests for the capstone WSGI application."""

import unittest

from app import application


class AppTest(unittest.TestCase):
    def call(self, path: str) -> tuple[str, bytes]:
        captured: list[str] = []

        def start(status: str, headers: list[tuple[str, str]]) -> None:
            captured.append(status)

        body = b"".join(application({"PATH_INFO": path}, start))
        return captured[0] if captured else "", body

    def test_health_and_ranked(self) -> None:
        self.assertEqual(self.call("/health")[0], "200 OK")
        self.assertIn(b"framework", self.call("/ranked")[1])

    def test_unknown_and_error_are_safe(self) -> None:
        self.assertEqual(self.call("/missing")[0], "404 Not Found")
        status, body = self.call("/boom")
        self.assertEqual(status, "500 Internal Server Error")
        self.assertNotIn(b"RuntimeError", body)


if __name__ == "__main__":
    unittest.main()
