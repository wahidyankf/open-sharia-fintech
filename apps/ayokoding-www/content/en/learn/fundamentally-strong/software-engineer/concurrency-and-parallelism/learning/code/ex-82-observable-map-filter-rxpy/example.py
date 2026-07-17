"""Example 82: An `Observable`, `map`, and `filter` -- Reactive Streams via `reactivex` (RxPY)."""

import reactivex  # => co-30: `reactivex` (RxPY 4.1.0) is the Python port of ReactiveX
from reactivex import operators as ops  # => operators live in their own module, chained via `.pipe()`


def build_pipeline() -> tuple[list[int], list[bool]]:
    collected: list[int] = []  # => collected: every value that reaches the FINAL observer's on_next
    completed_flag: list[bool] = []  # => completed_flag: appended to ONCE, when on_completed fires

    source = reactivex.from_iterable(range(10))  # => source: an Observable emitting 0, 1, 2, ..., 9, then completes
    pipeline = source.pipe(  # => `.pipe()` chains operators -- each one wraps/transforms the stream
        ops.map(lambda x: x * x),  # => map: transforms EVERY emitted value -- here, squares it
        ops.filter(lambda x: x % 2 == 0),  # => filter: only lets THROUGH values matching the predicate
    )  # => pipeline: an Observable of squares, but ONLY the even ones

    pipeline.subscribe(  # => subscribe: this is what ACTUALLY starts the stream flowing -- nothing runs before this
        on_next=collected.append,  # => on_next: called once PER item that survives map AND filter
        on_completed=lambda: completed_flag.append(True),  # => on_completed: called exactly once, after the LAST item
    )
    return collected, completed_flag  # => everything the caller needs to verify the pipeline's behavior


if __name__ == "__main__":  # => module entry point
    collected, completed_flag = build_pipeline()  # => drives the whole Observable pipeline to completion
    print(f"collected={collected}")  # => Output: collected=[0, 4, 16, 36, 64]
    print(f"completed={completed_flag}")  # => Output: completed=[True]

    expected = [n * n for n in range(10) if (n * n) % 2 == 0]  # => expected: squares of 0..9, keeping only even ones

    # => `map` and `filter` here work EXACTLY like their Python builtin namesakes conceptually, but
    # => operate on a PUSH-based stream (co-30) instead of a pull-based iterable: values are pushed
    # => through `map` (transform), then `filter` (keep-or-drop), landing at the final subscriber's
    # => `on_next` ONLY if they survive both stages. Nothing runs until `.subscribe()` is called --
    # => an Observable pipeline is a description of a computation, not the computation itself, until then.
    assert collected == expected  # => confirms only the TRANSFORMED, MATCHING items reached the observer
    assert completed_flag == [True]  # => confirms on_completed fired exactly once, after every item
    print("ex-82 OK")  # => Output: ex-82 OK
