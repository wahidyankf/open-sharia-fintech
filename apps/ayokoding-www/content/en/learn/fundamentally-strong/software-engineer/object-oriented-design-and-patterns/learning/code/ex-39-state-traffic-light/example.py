"""Example 39: Cycling States via the State Pattern."""

import abc  # => imports the abc module


class TrafficLight:  # => the CONTEXT -- holds whichever LightState object is CURRENT
    def __init__(self) -> None:  # => the constructor
        self.state: "LightState" = RedState()  # => every light starts at Red

    def next(self) -> str:  # => delegates "what comes next" to the CURRENT state object
        self.state = self.state.next_state()  # => the current state DECIDES its successor
        return self.state.name()  # => returns this value to the caller


class LightState(abc.ABC):  # => one state object PER color, not an enum with a switch
    @abc.abstractmethod
    def next_state(self) -> "LightState":  # => no body -- required by every color
        ...  # => the ellipsis stub -- concrete states below fill this in

    @abc.abstractmethod
    def name(self) -> str:  # => no body -- required by every color
        ...  # => the ellipsis stub -- concrete states below fill this in


class RedState(LightState):  # => Red always transitions to Green next
    def next_state(self) -> LightState:  # => defines the next_state() method
        return GreenState()  # => Red -> Green, and ONLY Red -> Green

    def name(self) -> str:  # => defines the name() method
        return "red"  # => returns this value to the caller


class GreenState(LightState):  # => Green always transitions to Yellow next
    def next_state(self) -> LightState:  # => defines the next_state() method
        return YellowState()  # => Green -> Yellow, and ONLY Green -> Yellow

    def name(self) -> str:  # => defines the name() method
        return "green"  # => returns this value to the caller


class YellowState(LightState):  # => Yellow always transitions back to Red
    def next_state(self) -> LightState:  # => defines the next_state() method
        return RedState()  # => Yellow -> Red, closing the cycle

    def name(self) -> str:  # => defines the name() method
        return "yellow"  # => returns this value to the caller


light: TrafficLight = TrafficLight()  # => constructs light, starting at Red
print(light.state.name())  # => the initial state, before any next() call
# => Output: red
print(light.next())  # => Red -> Green
# => Output: green
print(light.next())  # => Green -> Yellow
# => Output: yellow
print(light.next())  # => Yellow -> Red, the cycle repeats
# => Output: red
# => Each LightState object owns its OWN transition rule -- `next()` never branches on the color by name
