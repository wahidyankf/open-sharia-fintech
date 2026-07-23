"""Example 36: pytest verification for Command Objects with execute()/undo()."""

from example import AppendCommand, Command, Editor


def test_undo_reverses_only_the_most_recently_executed_command() -> None:
    editor: Editor = Editor()
    history: list[Command] = []
    for chunk in ["Hello", ", ", "World"]:
        cmd: Command = AppendCommand(editor, chunk)
        cmd.execute()
        history.append(cmd)
    assert editor.text == "Hello, World"  # => all three edits applied, in order

    history.pop().undo()  # => undoes only "World"
    assert editor.text == "Hello, "  # => the two earlier edits are still intact


# => Run: pytest -- Output: 1 passed
