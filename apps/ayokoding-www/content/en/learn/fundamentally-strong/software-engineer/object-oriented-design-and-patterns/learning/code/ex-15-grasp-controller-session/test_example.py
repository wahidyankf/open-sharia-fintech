"""Example 15: pytest verification for Controller: Route Events Through a Session Controller."""

import inspect

from example import SessionController, ShoppingCart, simulate_click


def test_ui_function_is_typed_against_the_controller_not_the_domain() -> None:
    signature: inspect.Signature = inspect.signature(simulate_click)  # => reads simulate_click's real parameter types
    controller_param = signature.parameters["controller"]
    assert controller_param.annotation is SessionController  # => the UI never names ShoppingCart in its own signature


def test_clicking_through_the_controller_mutates_the_cart() -> None:
    cart: ShoppingCart = ShoppingCart()
    controller: SessionController = SessionController(cart)
    simulate_click(controller, "widget", 9.99)  # => the ONE call the UI ever makes
    assert round(cart.total(), 2) == 9.99  # => the domain change genuinely happened


# => Run: pytest -- Output: 2 passed
