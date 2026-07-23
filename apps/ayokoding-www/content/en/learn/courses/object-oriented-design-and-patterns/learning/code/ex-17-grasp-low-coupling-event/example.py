"""Example 17: Low Coupling: Decouple via an Event Bus."""  # => module docstring

from typing import Callable  # => Callable types the event handlers the bus stores


class EventBus:  # => the ONLY object either module below depends on
    def __init__(self) -> None:  # => the constructor
        self._subscribers: dict[str, list[Callable[[int], None]]] = {}  # => event -> handlers
        # => GRASP's Low Coupling: both modules depend on this bus, never on each other

    def subscribe(  # => the registration method, spread across lines
        self,  # => the EventBus instance itself
        event: str,  # => the event NAME being subscribed to, a plain string key
        handler: Callable[[int], None],
        # => handler is stored generically -- the bus never inspects who registered it
    ) -> None:  # => defines the subscribe() method
        self._subscribers.setdefault(event, []).append(handler)  # => records the handler

    def publish(self, event: str, quantity: int) -> None:  # => defines the publish() method
        for handler in self._subscribers.get(
            event,
            [],  # => an empty list if nobody subscribed -- publish() never fails
        ):  # => calls every handler registered for this event
            handler(quantity)  # => the bus never knows WHAT a handler does
            # => low coupling: the bus is the ONLY thing either module depends on


class OrderModule:  # => publishes an event -- never imports or calls the other module
    def __init__(self, bus: EventBus) -> None:  # => the constructor
        self.bus = bus  # => the ONLY collaborator OrderModule holds

    def place_order(self, quantity: int) -> None:  # => defines the place_order() method
        self.bus.publish("order_placed", quantity)  # => announces the event, nothing more


class InventoryModule:  # => subscribes to an event -- never imports or calls the other module
    def __init__(self, bus: EventBus) -> None:  # => the constructor
        self.stock = 100  # => starting stock level
        bus.subscribe("order_placed", self._on_order_placed)  # => reacts to a named EVENT, never to a concrete publisher class

    def _on_order_placed(self, quantity: int) -> None:  # => the registered handler
        self.stock -= quantity  # => decrements stock in response to the event


bus: EventBus = EventBus()  # => constructs bus
inventory: InventoryModule = InventoryModule(bus)  # => subscribes itself to the bus
order_module: OrderModule = OrderModule(bus)  # => holds only the bus, nothing else

order_module.place_order(10)  # => OrderModule never calls InventoryModule directly
print(inventory.stock)  # => confirms InventoryModule reacted anyway, via the event
# => a THIRD module could subscribe to "order_placed" with no edit to either class above
# => Output: 90
# => Neither module's source code mentions the other module's class name at all
