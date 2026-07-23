"""Example 11: Replace a Train Wreck with Tell, Don't Ask."""


class Engine:  # => the innermost collaborator, two levels deep from Driver
    def ignite(self) -> str:  # => defines the ignite() method
        return "engine roars to life"  # => a real, honest implementation


class Car:  # => sits BETWEEN Driver and Engine
    def __init__(self, engine: Engine) -> None:  # => the constructor
        self.engine = engine  # => Car holds an Engine; Driver should never reach past Car

    def start(self) -> str:  # => Car's own tell-don't-ask method
        return self.engine.ignite()  # => Car delegates to its OWN collaborator, internally


class Driver:  # => the outermost caller
    def __init__(self, car: Car) -> None:  # => the constructor
        self.car = car  # => Driver holds a Car; that is the ONE dot Driver is allowed

    def start_car(self) -> str:  # => Driver's own tell-don't-ask method
        return self.car.start()  # => a single dot -- Driver never reaches into car.engine


def train_wreck_start(driver: Driver) -> str:  # => the BEFORE shape, shown for contrast
    return driver.car.engine.ignite()  # => two dots past driver -- a genuine train wreck


driver: Driver = Driver(Car(Engine()))  # => three collaborators, wired together once

wreck_result: str = train_wreck_start(driver)  # => works, but reaches through TWO objects
clean_result: str = driver.start_car()  # => the AFTER shape: exactly one dot from driver

print(wreck_result == clean_result)  # => same outcome, very different coupling
# => Output: True
# => `driver.start_car()` is the one-dot call; `driver.car.engine.ignite()` is the train wreck it replaces
