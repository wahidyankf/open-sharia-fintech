"""Example 1: name behaviour after the booking domain."""


class Booking:
    def __init__(self) -> None:
        self.confirmed = False  # => the domain state starts unconfirmed

    def confirm(self) -> None:
        self.confirmed = True  # => the business action changes one named fact


booking = Booking()  # => a reader can say what this object represents
booking.confirm()  # => no generic process() obscures the domain action
assert booking.confirmed  # => the domain sentence is directly testable
print("booking confirmed")  # => Output: booking confirmed
