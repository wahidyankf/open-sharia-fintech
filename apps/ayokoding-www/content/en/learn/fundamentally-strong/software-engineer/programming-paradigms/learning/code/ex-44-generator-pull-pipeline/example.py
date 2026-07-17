"""Example 44: Generator Pull Pipeline."""

from collections.abc import Callable, Iterator  # => every function below is typed as a lazy, pull-based Iterator

computed_log: list[int] = []  # => records every value the source generator actually produced


def source() -> Iterator[int]:  # => an "infinite" source -- would hang if fully consumed eagerly
    n = 0  # => starts at 0, incremented once per pull
    while True:  # => never terminates on its own -- laziness is the only thing that makes this safe
        n += 1  # => the next candidate value
        computed_log.append(n)  # => record that this value was actually generated (proves pull, not push)
        yield n  # => PULL-based: this line only runs when something asks the generator for its next value


def gen_map(it: Iterator[int], fn: Callable[[int], int]) -> Iterator[int]:  # => lazy map: transforms values ONE AT A TIME, on demand
    for value in it:  # => pulling from `it` only happens as this generator itself is pulled from
        yield fn(value)  # => nothing is computed until a consumer asks for the next item


def gen_filter(it: Iterator[int], predicate: Callable[[int], bool]) -> Iterator[int]:  # => lazy filter: same pull-based contract
    for value in it:  # => each pull here triggers exactly one pull upstream
        if predicate(value):  # => only values passing the predicate are ever yielded downstream
            yield value  # => only yield values that pass the predicate


def take(it: Iterator[int], n: int) -> list[int]:  # => the ONLY thing that actually drives the pipeline
    result: list[int] = []  # => the concrete list being built, one pull at a time
    for value in it:  # => pulling n times cascades back through filter -> map -> source
        result.append(value)  # => record this match before checking whether we have enough yet
        if len(result) == n:  # => stop pulling the instant we have enough -- laziness in action
            break  # => no further pulls happen -- the upstream generators simply stay paused
    return result  # => exactly n items, and not one pull more than strictly needed to produce them


pipeline = gen_filter(gen_map(source(), lambda n: n * n), lambda n: n % 2 == 0)  # => squares, then evens only
result = take(pipeline, 3)  # => pull exactly 3 matching items -- nothing more

print(result)  # => squares of 1..: 1,4,9,16,25,36,... ; even ones in order: 4, 16, 36
# => Output: [4, 16, 36]
print(len(computed_log))  # => the source only ran as many times as strictly needed to produce 3 matches
# => Output: 6
