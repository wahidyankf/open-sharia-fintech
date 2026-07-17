"""Kata 4 (after): ISP -- two narrow protocols; SimpleScrewdriver only implements the one it genuinely supports."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Screwable(Protocol):
    def screw(self) -> str: ...


@runtime_checkable
class Sawable(Protocol):
    def saw(self) -> str: ...


class SimpleScrewdriver:  # => implements ONLY Screwable -- no stubbed, wrong-behavior saw()
    def screw(self) -> str:
        return "screwed"


print(isinstance(SimpleScrewdriver(), Sawable))  # False -- the type system itself catches the mismatch now
