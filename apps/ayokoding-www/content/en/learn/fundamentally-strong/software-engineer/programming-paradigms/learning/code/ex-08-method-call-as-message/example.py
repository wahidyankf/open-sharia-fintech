"""Example 8: Method Call As Message."""

from typing import Protocol


class Speaker(Protocol):  # => the "message" every speaker must understand: speak()
    def speak(self) -> str: ...  # => the shape of the message, not its implementation


class Duck:  # => one concrete responder to the speak() message
    def speak(self) -> str:  # => Duck's own understanding of "speak"
        return "Quack"  # => Duck-specific reply


class Dog:  # => a second, unrelated (no shared base class) responder
    def speak(self) -> str:  # => Dog's own understanding of "speak"
        return "Woof"  # => Dog-specific reply


def announce(speaker: Speaker) -> str:  # => the caller only knows "send speak() to whatever this is"
    return speaker.speak()  # => this line is the MESSAGE SEND -- it does not know which class replies


animals: list[Speaker] = [Duck(), Dog()]  # => a mixed list -- no shared inheritance needed (structural)
for animal in animals:  # => iterate and send the same message to each
    print(announce(animal))  # => each object DISPATCHES the message to its own implementation
# => Output: Quack
# => Output: Woof
