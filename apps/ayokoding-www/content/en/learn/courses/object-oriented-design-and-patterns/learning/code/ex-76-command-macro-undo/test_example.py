"""Example 76: pytest verification that MacroCommand groups undo atomically, in reverse order."""

from example import DeleteLastCommand, InsertCommand, MacroCommand, TextBuffer


def test_macro_do_runs_every_sub_command_forward_in_order() -> None:
    buffer = TextBuffer()
    macro = MacroCommand([InsertCommand(buffer, "hello "), InsertCommand(buffer, "world")])
    macro.do()
    assert buffer.text == "hello world"


def test_macro_undo_reverses_every_sub_command_in_reverse_order_as_one_atomic_step() -> None:
    buffer = TextBuffer()
    macro = MacroCommand(
        [
            InsertCommand(buffer, "hello "),
            InsertCommand(buffer, "world"),
            DeleteLastCommand(buffer, 1),
        ]
    )
    macro.do()
    assert buffer.text == "hello worl"
    macro.undo()
    assert buffer.text == ""  # => a SINGLE undo() call reversed all three steps, atomically


def test_undo_never_leaves_the_buffer_in_a_partially_undone_intermediate_state() -> None:
    buffer = TextBuffer()
    macro = MacroCommand([InsertCommand(buffer, "a"), InsertCommand(buffer, "b"), InsertCommand(buffer, "c")])
    macro.do()
    assert buffer.text == "abc"
    macro.undo()
    assert buffer.text == ""  # => not "ab" or "a" -- the whole group undoes together, no partial state observed


# => Run: pytest -q -- Output: 3 passed
