"""Example 76: Dataflow vs Callback."""

from collections.abc import Callable, Iterator  # => Iterator types the dataflow style; Callable types the callback style


def pipeline_as_generators(nums: list[int]) -> Iterator[int]:  # => DATAFLOW: linear, pull-based stages
    doubled = (n * 2 for n in nums)  # => stage 1: a lazy generator expression
    evens = (n for n in doubled if n % 4 == 0)  # => stage 2: filters the output of stage 1
    labeled = (n for n in evens)  # => stage 3: a no-op stage, kept to show three composed stages
    return labeled  # => the caller pulls values through all three stages by iterating this


def pipeline_as_nested_callbacks(nums: list[int], on_result: Callable[[int], None]) -> None:  # => EVENT: nested calls
    def stage1(n: int, next_stage: Callable[[int], None]) -> None:  # => callback style: each stage CALLS the next
        next_stage(n * 2)  # => rather than returning a value, it invokes the next callback directly

    def stage2(n: int, next_stage: Callable[[int], None]) -> None:  # => callback style's own filtering stage
        if n % 4 == 0:  # => same filter as the generator's stage 2
            next_stage(n)  # => calling forward is the ONLY way this item continues down the pipeline
        # => note: an item filtered out here simply never calls next_stage -- no explicit "skip" needed

    def stage3(n: int, next_stage: Callable[[int], None]) -> None:  # => same no-op stage, for parity
        next_stage(n)  # => forwards to on_result via the nested lambda chain below

    for n in nums:  # => the caller still drives ITERATION, but each item cascades through nested calls
        stage1(n, lambda x: stage2(x, lambda y: stage3(y, on_result)))  # => three levels of nested callbacks


data = [1, 2, 3, 4, 5]  # => shared input for both styles

dataflow_result = list(pipeline_as_generators(data))  # => drain the lazy pipeline into a concrete list
print(dataflow_result)  # => doubled: 2,4,6,8,10; %4==0: 4, 8
# => Output: [4, 8]

callback_result: list[int] = []  # => the callback style delivers results via a side-effecting sink
pipeline_as_nested_callbacks(data, lambda n: callback_result.append(n))  # => drive it with a collecting callback
print(callback_result)  # => must be identical to the dataflow version's output
# => Output: [4, 8]
print(dataflow_result == callback_result)  # => same computation, radically different control-flow shape
# => Output: True
