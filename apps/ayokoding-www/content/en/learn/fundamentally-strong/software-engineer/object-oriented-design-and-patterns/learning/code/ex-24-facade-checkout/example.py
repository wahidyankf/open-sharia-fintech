"""Example 24: Facade: One Call Hides Three Subsystems."""  # => module docstring


class Inventory:  # => subsystem ONE -- the caller never touches this directly
    def reserve(self, item: str, qty: int) -> bool:  # => reserves stock for an order
        return qty <= 10  # => a simplified stock check, always succeeds for qty <= 10


class Payment:  # => subsystem TWO -- the caller never touches this directly
    def charge(self, amount: float) -> bool:  # => charges the customer
        return amount > 0  # => a simplified charge check, succeeds for any positive amount


class Shipping:  # => subsystem THREE -- the caller never touches this directly
    def schedule(self, item: str) -> str:  # => schedules delivery
        return f"{item} scheduled for delivery"  # => a real, honest implementation


class CheckoutFacade:  # => the FACADE -- one simplified entry point over all three
    def __init__(self) -> None:  # => the constructor
        self._inventory = Inventory()  # => wires subsystem one internally
        self._payment = Payment()  # => wires subsystem two internally
        self._shipping = Shipping()  # => wires subsystem three internally

    def checkout(  # => the SIMPLIFIED entry point, spread across lines
        self,  # => the CheckoutFacade instance, already wired to all three subsystems
        item: str,  # => a plain value, never a subsystem object
        qty: int,  # => a plain value, never a subsystem object
        amount: float,
        # => the caller passes plain values -- never an Inventory, Payment, or Shipping object
    ) -> str:  # => the ONE method the caller ever needs to call
        if not self._inventory.reserve(item, qty):  # => step one, hidden inside checkout()
            return "out of stock"  # => an early, honest failure
        if not self._payment.charge(amount):  # => step two, hidden inside checkout()
            return "payment failed"  # => an early, honest failure
        return self._shipping.schedule(item)  # => step three, the final hidden call


facade: CheckoutFacade = CheckoutFacade()  # => constructs facade, wiring all three internally
result: str = facade.checkout(
    "widget",  # => the item name, forwarded to Inventory and Shipping internally
    2,  # => the quantity, forwarded to Inventory internally
    9.99,  # => the amount, forwarded to Payment internally
    # => three subsystem calls happen inside checkout(), invisible from here
)  # => the caller's ONE call -- no Inventory, Payment, or Shipping mentioned here

print(result)  # => confirms all three subsystems cooperated behind one call
# => a caller unfamiliar with Inventory/Payment/Shipping can still complete a checkout
# => Output: widget scheduled for delivery
# => The caller never imports `Inventory`, `Payment`, or `Shipping` -- only `CheckoutFacade`
