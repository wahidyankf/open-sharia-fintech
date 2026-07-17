"""Example 36: Command Objects with execute()/undo() for an Editor."""

import abc  # => imports the abc module


class Editor:  # => the RECEIVER -- the object commands actually act upon
    def __init__(self) -> None:  # => the constructor
        self.text: str = ""  # => the editor's own, mutable document content

    def append(self, chunk: str) -> None:  # => defines the append() method
        self.text += chunk  # => the low-level operation a Command wraps

    def remove_last(self, length: int) -> None:  # => defines the remove_last() method
        self.text = self.text[:-length]  # => the low-level UNDO operation


class Command(abc.ABC):  # => reifies a REQUEST as an object, with both directions
    @abc.abstractmethod
    def execute(self) -> None:  # => no body -- required by every concrete command
        ...  # => the ellipsis stub -- AppendCommand below fills this in

    @abc.abstractmethod
    def undo(self) -> None:  # => no body -- required by every concrete command
        ...  # => the ellipsis stub -- AppendCommand below fills this in


class AppendCommand(Command):  # => a CONCRETE command wrapping one append operation
    def __init__(self, editor: Editor, chunk: str) -> None:  # => the constructor
        self._editor: Editor = editor  # => the receiver this command acts on
        self._chunk: str = chunk  # => remembers WHAT it appended, needed to undo later

    def execute(self) -> None:  # => defines the execute() method
        self._editor.append(self._chunk)  # => delegates to the receiver's low-level op

    def undo(self) -> None:  # => defines the undo() method
        self._editor.remove_last(len(self._chunk))  # => reverses exactly what execute() did


history: list[Command] = []  # => a stack of EXECUTED commands, most recent last
editor: Editor = Editor()  # => constructs editor

for chunk in ["Hello", ", ", "World"]:  # => three separate edits, one command each
    cmd: Command = AppendCommand(editor, chunk)  # => wraps this edit as a Command object
    cmd.execute()  # => performs the edit
    history.append(cmd)  # => remembered so it can be undone later, in reverse order

print(editor.text)  # => all three chunks appended, in order
# => Output: Hello, World

last: Command = history.pop()  # => the MOST RECENT command, undone first
last.undo()  # => reverses only the last edit, "World"
print(editor.text)  # => "World" is gone -- the two earlier edits remain intact
# => Output: Hello,
# => Wrapping each edit as a Command object turns "undo the last thing" into `history.pop().undo()`
