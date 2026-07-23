"""Example 15: Controller: Route Events Through a Session Controller."""  # => docstring


class ShoppingCart:  # => the DOMAIN class -- pure business logic, no UI concerns
    def __init__(self) -> None:  # => the constructor
        self.items: list[tuple[str, float]] = []  # => (name, price) pairs held here

    def add_item(self, name: str, price: float) -> None:  # => domain-level mutation
        self.items.append((name, price))  # => the domain's own state change

    def total(self) -> float:  # => defines the total() method
        return sum(price for _, price in self.items)  # => sums every stored price


class SessionController:  # => the CONTROLLER -- the single coordinator between UI and domain
    def __init__(self, cart: ShoppingCart) -> None:  # => the constructor
        self.cart = cart  # => holds the domain object the UI is never handed directly
        # => GRASP's Controller: one coordinating object, not the UI, talks to the domain

    def handle_add_item_event(  # => the single ENTRY POINT, spread across lines
        self,
        name: str,  # => raw event data, not yet a domain call
        price: float,
        # => a UI event comes IN here; the domain call happens INSIDE this method
    ) -> None:  # => the ONE entry point every UI click routes through
        self.cart.add_item(name, price)  # => forwards to the domain, safely coordinated


def simulate_click(  # => a free function standing in for a real UI event handler
    controller: SessionController,  # => the UI's only handle on the domain -- via the controller
    name: str,
    price: float,
    # => the UI layer's type hint names SessionController, never ShoppingCart
) -> None:  # => simulates a UI event handler firing
    controller.handle_add_item_event(name, price)  # => the UI never calls cart.add_item() directly, ever


cart: ShoppingCart = ShoppingCart()  # => constructs cart
controller: SessionController = SessionController(cart)  # => constructs controller
# => the UI code below never sees `cart` directly -- only `controller`
simulate_click(controller, "widget", 9.99)  # => routed entirely through the controller

print(round(cart.total(), 2))  # => confirms the domain state actually changed
# => proof the event reached ShoppingCart WITHOUT the UI ever naming ShoppingCart
# => Output: 9.99
# => Every UI event flows through `SessionController` -- the UI layer never imports `ShoppingCart`'s mutation methods
