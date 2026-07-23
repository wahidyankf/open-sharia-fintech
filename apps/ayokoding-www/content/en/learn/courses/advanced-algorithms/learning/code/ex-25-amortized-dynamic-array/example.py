"""Example 25: A Doubling Dynamic Array -- Amortized O(1) Append, Counted."""

# list.append is amortized O(1) because resizes DOUBLE capacity (co-02):
# rare, expensive O(n) copies are outweighed by many cheap O(1) appends in
# between. This example implements that doubling explicitly and COUNTS copies.


class DynamicArray:  # => a from-scratch array that grows by doubling, like CPython's
    def __init__(self) -> None:
        self.capacity: int = 1  # => starts with room for exactly 1 element
        self.size: int = 0  # => how many elements are actually stored so far
        self.data: list[int | None] = [None] * self.capacity  # => the backing storage
        self.total_copies: int = 0  # => running count of element copies during resizes

    def append(self, value: int) -> None:  # => amortized O(1) per call
        if self.size == self.capacity:  # => backing storage is full -- must grow
            self._resize(self.capacity * 2)  # => DOUBLING is what makes this amortized
        self.data[self.size] = value  # => O(1): writes into the next free slot
        self.size += 1  # => one more element stored

    def _resize(self, new_capacity: int) -> None:  # => O(n): the rare, expensive step
        new_data: list[int | None] = [None] * new_capacity  # => a fresh, larger array
        for i in range(self.size):  # => copies every EXISTING element over
            new_data[i] = self.data[i]  # => one copy per existing element
            self.total_copies += 1  # => tallies this copy for the amortized-cost check
        self.data = new_data  # => the array now points at the larger backing storage
        self.capacity = new_capacity  # => capacity reflects the new, larger size


arr = DynamicArray()  # => starts empty, capacity 1
n = 1000  # => how many appends to perform
for i in range(n):  # => n appends -- MOST are O(1), a few trigger an O(n) resize
    arr.append(i)  # => amortized O(1) each

average_copies_per_append = arr.total_copies / n  # => the amortized cost per append
print(arr.size)  # => Output: 1000
print(arr.total_copies)  # => Output: 1023 -- sum of 1+2+4+...+512, just over n
print(f"{average_copies_per_append:.3f}")  # => Output: 1.023

assert arr.size == n  # => confirms every append landed correctly
assert (
    average_copies_per_append < 2.0
)  # => confirms the amortized cost stays BOUNDED by a small constant, not O(n)
print("ex-25 OK")  # => Output: ex-25 OK
