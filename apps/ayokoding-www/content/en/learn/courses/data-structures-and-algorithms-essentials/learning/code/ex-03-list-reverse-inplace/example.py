"""Example 3: List Reverse In Place."""

# .reverse() mutates the SAME list object -- no new list is allocated (co-03).
order: list[int] = [1, 2, 3, 4]  # => order is [1, 2, 3, 4]
same_object = order  # => same_object is another name for the SAME list, not a copy
order.reverse()  # => reverses the elements of order in place, O(n)
print(order)  # => Output: [4, 3, 2, 1]
print(same_object)  # => same_object sees the mutation too -- Output: [4, 3, 2, 1]

assert order == [4, 3, 2, 1]  # => confirms the reversed order matches expected
assert same_object is order  # => confirms .reverse() did NOT create a new list object
print("ex-03 OK")  # => Output: ex-03 OK
