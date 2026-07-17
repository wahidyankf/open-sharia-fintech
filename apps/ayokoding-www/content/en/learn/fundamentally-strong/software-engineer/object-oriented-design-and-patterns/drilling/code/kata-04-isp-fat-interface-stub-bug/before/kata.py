"""Kata 4 (before): ISP violation -- a fat interface forces an unrelated stub, causing a silent wrong-behavior bug."""

from abc import ABC, abstractmethod


class MultiTool(ABC):  # SMELL: bundles unrelated capabilities into one fat interface
    @abstractmethod
    def screw(self) -> str: ...

    @abstractmethod
    def saw(self) -> str: ...


class SimpleScrewdriver(MultiTool):
    def screw(self) -> str:
        return "screwed"

    def saw(self) -> str:
        return "screwed"  # BUG: stubbed to satisfy the ABC, but callers relying on saw() get the WRONG behavior


def use_saw(tool: MultiTool) -> str:
    return tool.saw()


print(use_saw(SimpleScrewdriver()))  # expected some sawing behavior -- gets "screwed" instead, silently wrong
