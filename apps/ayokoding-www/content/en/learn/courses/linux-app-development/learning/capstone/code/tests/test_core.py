from notes_linux.core import status_reply


def test_status_protocol():
    assert status_reply(b"STATUS") == b"OK notes-daemon"


def test_bad_command_has_error_reply():
    assert status_reply(b"OTHER").startswith(b"ERROR")
