"""Example 48: A staticmethod Namespaced Utility."""


class Date:  # => begins the Date class body
    @staticmethod  # => marks the next method as needing neither self nor cls
    def is_leap(
        year: int,
    ) -> bool:  # => neither self nor cls -- an ordinary function in a namespace
        return year % 4 == 0 and (
            year % 100 != 0 or year % 400 == 0
        )  # => returns this value to the caller


print(
    Date.is_leap(2024)
)  # => callable directly on the class -- no instance needed anywhere
# => Output: True
print(Date.is_leap(1900))  # => divisible by 100 but not 400 -- not a leap year
# => Output: False
# => `Date.is_leap(year)` never touches `self` or `cls`
