# learning/code/ex-30-stack-vs-heap-ids/stack_vs_heap.py
"""Example 30: A Local int vs. a Heap-Allocated List -- Contrasted via id()."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def make_local_int() -> int:  # => co-17: a plain int -- CPython still boxes it on the heap, but its NAME/frame is automatic
    """Return a small int computed and 'living' entirely within this frame's automatic lifetime."""  # => co-17: documents make_local_int's contract -- no runtime output, just sets its __doc__
    local_value = 41 + 1  # => co-17: this NAME (`local_value`) exists only while this frame is on the stack
    return local_value  # => co-17: the frame's own storage for `local_value` is reclaimed the instant this returns


def make_heap_list() -> list[int]:  # => co-17: the returned list object OUTLIVES this function's own frame
    """Build and return a list -- the object survives this frame's return, unlike a plain automatic local."""  # => co-17: documents make_heap_list's contract -- no runtime output, just sets its __doc__
    heap_object = [1, 2, 3]  # => co-17: heap_object is a NAME in this frame, but the LIST it names is heap-allocated
    return heap_object  # => co-17: the name `heap_object` dies with the frame; the OBJECT it pointed to does not


if __name__ == "__main__":  # => co-17: entry point -- this block runs only when the file executes directly, not on import
    returned_int = make_local_int()  # => co-17: make_local_int()'s frame has already been popped by this line
    print(f"returned_int = {returned_int}, id = {id(returned_int)}")  # => co-17: still usable -- ints are immutable values
    returned_list = make_heap_list()  # => co-17: make_heap_list()'s frame has ALSO already been popped
    list_id_after_return = id(returned_list)  # => co-17: the heap object's identity, observed AFTER its creating frame is gone
    print(f"returned_list = {returned_list}, id = {list_id_after_return}")  # => co-17: the object is still fully alive and usable
    returned_list.append(4)  # => co-17: mutating it here proves it's a REAL, live heap object -- not a stale reference
    print(f"after append: {returned_list}")  # => co-17: expect [1, 2, 3, 4] -- the object legitimately outlived its frame
    assert returned_list == [1, 2, 3, 4], "the heap list must remain mutable after its creating frame returned"  # => co-17
    assert id(returned_list) == list_id_after_return, "the object's identity must not change across the mutation"  # => co-17
    print(f"Heap object outlives its creating stack frame: True")  # => co-17: both asserts above passed
    # => co-17: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
