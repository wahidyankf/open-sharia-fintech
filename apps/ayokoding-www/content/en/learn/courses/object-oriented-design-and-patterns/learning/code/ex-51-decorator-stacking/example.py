"""Example 51: Stacking Retry + Cache + Log Decorators."""

from typing import Protocol  # => imports Protocol from typing


class Fetcher(Protocol):  # => the shared shape EVERY layer in the stack must match
    def __call__(self, key: str) -> str:  # => the shape every decorator must match
        ...  # => the ellipsis stub -- no implementation, just the contract


class BaseFetcher:  # => the innermost, REAL fetcher -- knows nothing about the wrappers
    def __init__(self, trace: list[str]) -> None:  # => the constructor
        self._trace: list[str] = trace  # => shared trace, so the example can OBSERVE order

    def __call__(self, key: str) -> str:  # => defines the __call__() method
        self._trace.append(f"fetch:{key}")  # => records that the REAL work happened
        return f"data-for-{key}"  # => returns this value to the caller


class LoggingDecorator:  # => the INNERMOST wrapper -- closest to BaseFetcher
    def __init__(self, inner: Fetcher, trace: list[str]) -> None:  # => the constructor
        self._inner: Fetcher = inner  # => the layer THIS decorator wraps
        self._trace: list[str] = trace  # => shared trace, so the example can OBSERVE order

    def __call__(self, key: str) -> str:  # => defines the __call__() method
        self._trace.append(f"log:enter:{key}")  # => runs BEFORE delegating inward
        result: str = self._inner(key)  # => delegates to the wrapped layer
        self._trace.append(f"log:exit:{key}")  # => runs AFTER delegating inward
        return result  # => returns this value to the caller


class CachingDecorator:  # => the MIDDLE wrapper -- can SKIP the inner layers entirely
    def __init__(self, inner: Fetcher, trace: list[str]) -> None:  # => the constructor
        self._inner: Fetcher = inner  # => the layer THIS decorator wraps
        self._trace: list[str] = trace  # => shared trace, so the example can OBSERVE order
        self._cache: dict[str, str] = {}  # => this layer's OWN state, invisible to the others

    def __call__(self, key: str) -> str:  # => defines the __call__() method
        if key in self._cache:  # => a cache HIT skips every layer wrapped by this one
            self._trace.append(f"cache:hit:{key}")  # => records the skip explicitly
            return self._cache[key]  # => returns this value to the caller
        self._trace.append(f"cache:miss:{key}")  # => records that inner layers WILL run
        result: str = self._inner(key)  # => only reached on a cache MISS
        self._cache[key] = result  # => stores the result for the NEXT call with this key
        return result  # => returns this value to the caller


class RetryDecorator:  # => the OUTERMOST wrapper -- what the caller actually calls
    def __init__(self, inner: Fetcher, trace: list[str], max_attempts: int = 3) -> None:  # => the constructor
        self._inner: Fetcher = inner  # => the layer THIS decorator wraps
        self._trace: list[str] = trace  # => shared trace, so the example can OBSERVE order
        self._max_attempts: int = max_attempts  # => stores max_attempts on this instance

    def __call__(self, key: str) -> str:  # => defines the __call__() method
        self._trace.append(f"retry:enter:{key}")  # => runs BEFORE delegating inward
        result: str = self._inner(key)  # => delegates through Cache -> Log -> Base
        self._trace.append(f"retry:exit:{key}")  # => runs AFTER delegating inward
        return result  # => returns this value to the caller


trace: list[str] = []  # => a shared list every layer appends to, in CALL order
base: BaseFetcher = BaseFetcher(trace)  # => constructs base
logged: LoggingDecorator = LoggingDecorator(base, trace)  # => wraps base -- innermost decorator
cached: CachingDecorator = CachingDecorator(logged, trace)  # => wraps logged -- middle decorator
stack: RetryDecorator = RetryDecorator(cached, trace)  # => wraps cached -- outermost decorator

first: str = stack("user-1")  # => a cache MISS -- every layer runs, in outer-to-inner order
print(first)  # => the value BaseFetcher actually produced
# => Output: data-for-user-1
print(trace)  # => confirms the exact outer -> inner -> outer call sequence
# => Output: ['retry:enter:user-1', 'cache:miss:user-1', 'log:enter:user-1', 'fetch:user-1', 'log:exit:user-1', 'retry:exit:user-1']

trace.clear()  # => resets the trace so the SECOND call's order is easy to read in isolation
stack("user-1")  # => a cache HIT -- Log and Base are SKIPPED entirely
print(trace)  # => the cache short-circuits everything wrapped INSIDE it
# => Output: ['retry:enter:user-1', 'cache:hit:user-1', 'retry:exit:user-1']
# => The composition order (Retry -> Cache -> Log -> Base) determines WHICH layers run on a cache hit
