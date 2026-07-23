"""Example 37: Queueing Commands for Deferred Batch Execution."""

import abc  # => imports the abc module


class Command(abc.ABC):  # => reifies a REQUEST as an object, queueable like any value
    @abc.abstractmethod
    def execute(self) -> str:  # => no body -- required by every concrete command
        ...  # => the ellipsis stub -- concrete commands below fill this in


class SendEmailCommand(Command):  # => a CONCRETE command -- not run until the queue drains
    def __init__(self, to: str) -> None:  # => the constructor
        self._to: str = to  # => remembers WHAT to do, without doing it yet

    def execute(self) -> str:  # => defines the execute() method
        return f"email sent to {self._to}"  # => the actual side effect, deferred until now


class LogEventCommand(Command):  # => a DIFFERENT concrete command, same Command interface
    def __init__(self, message: str) -> None:  # => the constructor
        self._message: str = message  # => remembers WHAT to do, without doing it yet

    def execute(self) -> str:  # => defines the execute() method
        return f"logged: {self._message}"  # => the actual side effect, deferred until now


class CommandQueue:  # => holds commands as PLAIN DATA until something drains the queue
    def __init__(self) -> None:  # => the constructor
        self._pending: list[Command] = []  # => nothing executes just by being queued

    def enqueue(self, command: Command) -> None:  # => defines the enqueue() method
        self._pending.append(command)  # => appends WITHOUT calling execute() at all

    def run_all(self) -> list[str]:  # => the deferred batch execution step
        results: list[str] = [cmd.execute() for cmd in self._pending]  # => runs every queued command, in the EXACT order they were enqueued
        self._pending.clear()  # => the queue is empty once this batch has run
        return results  # => returns this value to the caller


queue: CommandQueue = CommandQueue()  # => constructs queue
queue.enqueue(LogEventCommand("user signed up"))  # => queued FIRST -- not yet executed
queue.enqueue(SendEmailCommand("new-user@example.com"))  # => queued SECOND -- not yet executed
queue.enqueue(LogEventCommand("welcome email queued"))  # => queued THIRD -- not yet executed

print(len(queue._pending))  # => nothing has executed yet -- just three unexecuted commands, queued
# => Output: 3
results: list[str] = queue.run_all()  # => the ENTIRE batch runs now, in enqueue order
for line in results:  # => prints each result on its own line
    print(line)  # => confirms execution happened in the SAME order commands were enqueued
# => Output: logged: user signed up
# => Output: email sent to new-user@example.com
# => Output: logged: welcome email queued
# => Queueing a Command defers its side effect; `run_all()` executes every queued command in enqueue order
