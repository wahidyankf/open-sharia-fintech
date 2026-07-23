"""Example 11: pytest verification for Replace a Train Wreck with Tell, Don't Ask."""

from example import Car, Driver, Engine


def test_start_car_produces_a_single_dot_call_site() -> None:
    driver: Driver = Driver(Car(Engine()))
    # => the caller reaches exactly one attribute deep: driver.start_car()
    result: str = driver.start_car()  # => never touches driver.car.engine directly
    assert result == "engine roars to life"


def test_delegation_chain_still_reaches_the_engine() -> None:
    driver: Driver = Driver(Car(Engine()))
    assert driver.start_car() == driver.car.engine.ignite()  # => same result, one call site is a train wreck and one is not


# => Run: pytest -- Output: 2 passed
