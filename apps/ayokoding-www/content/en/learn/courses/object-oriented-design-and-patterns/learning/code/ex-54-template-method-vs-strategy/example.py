"""Example 54: The Same Pipeline as Template Method and as Strategy."""

import abc  # => imports the abc module
from typing import Protocol  # => imports Protocol from typing


# => TEMPLATE METHOD: the base class owns the SKELETON, subclasses fill named steps
class PipelineTemplate(abc.ABC):  # => defines the fixed ALGORITHM shape once
    def run(self, data: str) -> str:  # => the SKELETON -- never overridden by subclasses
        cleaned: str = data.strip()  # => a shared, non-varying step
        processed: str = self._process(cleaned)  # => the ONE varying step, deferred
        return f"saved:{processed}"  # => a shared, non-varying step

    @abc.abstractmethod
    def _process(self, cleaned: str) -> str:  # => no body -- required by every subclass
        ...  # => the ellipsis stub -- concrete pipelines below fill this in


class UppercasePipeline(PipelineTemplate):  # => FIXED at class-definition time
    def _process(self, cleaned: str) -> str:
        return cleaned.upper()  # => returns this value to the caller


class ReversePipeline(PipelineTemplate):  # => a DIFFERENT subclass, a DIFFERENT fixed behavior
    def _process(self, cleaned: str) -> str:
        return cleaned[::-1]  # => returns this value to the caller


# => STRATEGY: the SAME skeleton, but the varying step is an object held on ONE class
class ProcessingStrategy(Protocol):  # => the shape every strategy must match
    def __call__(self, cleaned: str) -> str:  # => the shape every strategy must match
        ...  # => the ellipsis stub -- no shared base class required at all


def uppercase_strategy(cleaned: str) -> str:  # => a PLAIN function, satisfies the Protocol
    return cleaned.upper()  # => returns this value to the caller


def reverse_strategy(cleaned: str) -> str:  # => a DIFFERENT plain function, same shape
    return cleaned[::-1]  # => returns this value to the caller


class PipelineWithStrategy:  # => ONE class -- the varying step is a swappable FIELD, not a subclass
    def __init__(self, strategy: ProcessingStrategy) -> None:  # => the constructor
        self.strategy = strategy  # => held as ordinary, REASSIGNABLE instance state

    def run(self, data: str) -> str:  # => the SAME skeleton shape as PipelineTemplate.run()
        cleaned: str = data.strip()  # => a shared, non-varying step
        processed: str = self.strategy(cleaned)  # => the varying step, called through the field
        return f"saved:{processed}"  # => a shared, non-varying step


template_result: str = UppercasePipeline().run("  hello  ")  # => FIXED at construction time
print(template_result)  # => choosing behavior means choosing a DIFFERENT subclass
# => Output: saved:HELLO

pipeline: PipelineWithStrategy = PipelineWithStrategy(uppercase_strategy)  # => ONE instance, starts uppercase
print(pipeline.run("  hello  "))  # => the SAME instance, uppercase behavior
# => Output: saved:HELLO

pipeline.strategy = reverse_strategy  # => swaps behavior at RUNTIME, no new instance, no subclass
print(pipeline.run("  hello  "))  # => the SAME instance, now reversed -- runtime swap, not construction
# => Output: saved:olleh
# => Strategy swaps behavior on an EXISTING instance at runtime; Template Method fixes it per SUBCLASS at construction
