# learning/code/ex-29-stack-frame-trace/stack_frame_trace.py
"""Example 29: Recursive Factorial -- Call Frames Push Then Pop in Order."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

call_log: list[str] = []  # => co-17: records "push" and "pop" events, in the ACTUAL order they happen


def factorial(n: int, depth: int = 0) -> int:  # => co-17: each call is a new STACK FRAME with its own n, depth
    """Recursive factorial that logs frame push/pop events at every call depth."""  # => co-17: documents factorial's contract -- no runtime output, just sets its __doc__
    call_log.append(f"push depth={depth} n={n}")  # => co-17: a new frame is pushed onto the call stack HERE
    if n <= 1:  # => co-17: the base case -- the deepest frame, which pops immediately without recursing further
        call_log.append(f"pop  depth={depth} n={n} returns=1")  # => co-17: this frame's automatic-lifetime storage ends
        return 1  # => co-17: unwinds back to the caller -- the frame's local variables cease to exist
    result = n * factorial(n - 1, depth + 1)  # => co-17: a NEW frame is pushed for the recursive call, one level deeper
    call_log.append(f"pop  depth={depth} n={n} returns={result}")  # => co-17: THIS frame pops only after its callee returns
    return result  # => co-17: this frame's own local storage (n, depth, result) is reclaimed here


if __name__ == "__main__":  # => co-17: entry point -- this block runs only when the file executes directly, not on import
    call_log.clear()  # => co-17: fresh log for this run
    total = factorial(4)  # => co-17: 4! = 24, via 4 nested frames (depths 0 through 3, n=4 down to n=1)
    print(f"factorial(4) = {total}")  # => co-17: expect 24
    for line in call_log:  # => co-17: prints the frame push/pop sequence, in the exact order it happened
        print(f"  {line}")  # => co-17: every push must be followed, eventually, by a MATCHING pop
    pushes = [line for line in call_log if line.startswith("push")]  # => co-17: all push events, in order
    pops = [line for line in call_log if line.startswith("pop")]  # => co-17: all pop events, in order
    assert len(pushes) == len(pops) == 4, "every push must have a matching pop, 4 frames total"  # => co-17
    assert call_log[0].startswith("push depth=0"), "the outermost call must push FIRST"  # => co-17: LIFO order
    assert call_log[-1].startswith("pop  depth=0"), "the outermost call must pop LAST"  # => co-17: LIFO order
    assert total == 24, "factorial(4) must equal 24"  # => co-17: the arithmetic result itself
    print(f"Frames pushed then popped in correct LIFO order: True")  # => co-17: all asserts above passed
    # => co-17: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
