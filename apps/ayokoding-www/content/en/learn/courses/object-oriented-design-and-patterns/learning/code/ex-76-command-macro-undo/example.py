"""Example 76: Command -- Composite Macro Command With Grouped Undo.

co-27, co-23: a text-buffer editor where every edit is a Command object with
`do()`/`undo()`. A `MacroCommand` (co-23: composite -- a command made of
commands) groups several edits into one atomic unit: calling its `undo()`
reverses every sub-command in REVERSE order, so a multi-step edit undoes as a
single step, never leaving the buffer in a partially-undone state.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from typing import Protocol  # => Protocol declares the Command shape every do/undo pair must satisfy


# => every Command below holds a reference to THIS SAME buffer -- there is only ever one receiver in this example
class TextBuffer:  # => the receiver -- the object commands actually mutate
    def __init__(self) -> None:  # => the constructor
        self.text = ""  # => starts empty; every command below mutates THIS field


# => InsertCommand, DeleteLastCommand, and MacroCommand all satisfy THIS one shape, structurally
class Command(Protocol):  # => co-27: every command supports do/undo symmetrically
    def do(self) -> None: ...  # => the forward action
    def undo(self) -> None: ...  # => the reverse action, mirroring do() exactly


# => InsertCommand and DeleteLastCommand are LEAVES in the composite sense -- MacroCommand is the COMPOSITE node
class InsertCommand:  # => a concrete command: insert text at the end of the buffer
    def __init__(self, buffer: TextBuffer, text: str) -> None:  # => the constructor
        self._buffer = buffer  # => the receiver this command acts on
        self._text = text  # => remembers WHAT it inserted, needed later to undo

    def do(self) -> None:  # => satisfies Command's do() clause
        self._buffer.text += self._text  # => the forward action: appends the remembered text

    def undo(self) -> None:  # => satisfies Command's undo() clause
        self._buffer.text = self._buffer.text[: -len(self._text)]  # => removes exactly what was inserted


# => notice DeleteLastCommand needs internal state (_deleted) to undo -- InsertCommand needs none, it can recompute
# => remembering _deleted (not just _count) is what makes THIS command's undo() possible too
class DeleteLastCommand:  # => a second concrete command: delete the last N characters
    def __init__(self, buffer: TextBuffer, count: int) -> None:  # => the constructor
        self._buffer = buffer  # => the receiver this command acts on
        self._count = count  # => how many trailing characters to remove
        self._deleted = ""  # => remembers what was deleted, so undo() can restore it exactly

    def do(self) -> None:  # => satisfies Command's do() clause
        self._deleted = self._buffer.text[-self._count :]  # => captures the characters BEFORE removing them
        self._buffer.text = self._buffer.text[: -self._count]  # => the forward action: removes the trailing slice

    def undo(self) -> None:  # => satisfies Command's undo() clause
        self._buffer.text += self._deleted  # => restores the exact characters that were removed


# => MacroCommand satisfies the SAME Command shape as its own children -- the composite pattern's defining trait
class MacroCommand:  # => co-23: COMPOSITE -- a command built out of other commands, same Command interface
    def __init__(self, commands: list[Command]) -> None:  # => the constructor
        self._commands = commands  # => the ordered group of sub-commands this macro wraps

    def do(self) -> None:  # => satisfies Command's do() clause, delegating to every sub-command
        for command in self._commands:  # => forward order
            command.do()  # => each sub-command performs its own forward action

    def undo(self) -> None:  # => satisfies Command's undo() clause, delegating to every sub-command
        for command in reversed(self._commands):  # => co-27: REVERSE order -- undoes atomically as one unit
            command.undo()  # => each sub-command reverses its own forward action


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    buffer = TextBuffer()  # => the shared receiver every command below will mutate
    macro = MacroCommand(  # => groups three sub-commands into one atomic unit
        [  # => the ordered list handed to MacroCommand's constructor
            InsertCommand(buffer, "hello "),  # => sub-command 1: appends "hello "
            InsertCommand(buffer, "world"),  # => sub-command 2: appends "world"
            DeleteLastCommand(buffer, 1),  # => drops the trailing "d"
        ]  # => the list itself, not yet executed -- macro.do() below runs it
    )  # => closes the sub-command list passed to MacroCommand

    macro.do()  # => runs all three sub-commands forward, as one grouped edit
    print(repr(buffer.text))  # => shows the buffer after all three forward actions ran
    # => Output: 'hello worl'
    # => "hello " + "world" - "d" = "hello worl" -- three edits collapsed into one visible result

    macro.undo()  # => reverses all three, in REVERSE order, as one atomic undo
    print(repr(buffer.text))  # => confirms the buffer is back to its original, pre-macro state
    # => Output: ''
    # => undoing in REVERSE order matters: undoing "insert world" before "insert hello " would corrupt the slice math
