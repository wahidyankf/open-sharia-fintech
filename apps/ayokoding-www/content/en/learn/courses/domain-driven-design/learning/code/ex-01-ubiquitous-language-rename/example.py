# => Keeps this domain step explicit and reviewable.
"""Example 1: name behaviour after the booking domain."""


# => Gives domain rules a single, named home.
class Booking:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        self.confirmed = False  # => the domain state starts unconfirmed

    # => Names policy so callers do not recreate the rule.
    def confirm(self) -> None:
        self.confirmed = True  # => the business action changes one named fact


booking = Booking()  # => a reader can say what this object represents
booking.confirm()  # => no generic process() obscures the domain action
assert booking.confirmed  # => the domain sentence is directly testable
print("booking confirmed")  # => Output: booking confirmed
