"""Test stdout and stderr separately with pytest capsys."""

import sys


def emit_status():
    print("pending=2")
    print("notes: diagnostic", file=sys.stderr)


def test_streams_are_separate(capsys):
    emit_status()
    captured = capsys.readouterr()
    assert captured.out == "pending=2\n"
    assert captured.err == "notes: diagnostic\n"
