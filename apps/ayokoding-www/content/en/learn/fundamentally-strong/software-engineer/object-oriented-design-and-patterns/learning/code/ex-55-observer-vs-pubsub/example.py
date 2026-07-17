"""Example 55: Direct Observer vs a Decoupling Pub/Sub Broker."""

import abc  # => imports the abc module


# => DIRECT OBSERVER: the Subject holds CONCRETE Observer objects, and imports the type
class Observer(abc.ABC):  # => the Subject depends on THIS type directly
    @abc.abstractmethod
    def update(self, price: float) -> None:  # => no body -- required by every observer
        ...  # => the ellipsis stub -- concrete observers below fill this in


class StockSubject:  # => holds a list of Observer OBJECTS -- a direct, typed reference
    def __init__(self) -> None:  # => the constructor
        self._observers: list[Observer] = []  # => the Subject KNOWS the Observer type

    def attach(self, observer: Observer) -> None:  # => defines the attach() method
        self._observers.append(observer)  # => accepts only things typed as Observer

    def set_price(self, price: float) -> None:  # => defines the set_price() method
        for observer in self._observers:  # => notifies every attached Observer DIRECTLY
            observer.update(price)  # => calls a method on a CONCRETE type it imports


class PriceLogger(Observer):  # => a concrete Observer -- must satisfy the imported interface
    def __init__(self) -> None:  # => the constructor
        self.history: list[float] = []  # => stores history on this instance

    def update(self, price: float) -> None:  # => defines the update() method
        self.history.append(price)  # => records the update


# => PUB/SUB BROKER: the publisher never references Observer, or any subscriber type, at all
class EventBroker:  # => the ONLY thing that knows about subscriber CALLABLES
    def __init__(self) -> None:  # => the constructor
        self._subscribers: dict[str, list[object]] = {}  # => topic -> list of PLAIN callables

    def subscribe(self, topic: str, callback: object) -> None:  # => defines subscribe()
        self._subscribers.setdefault(topic, []).append(callback)  # => stores it opaquely

    def publish(self, topic: str, value: float) -> None:  # => defines the publish() method
        for callback in self._subscribers.get(topic, []):  # => calls each stored callable
            callback(value)  # type: ignore  # => a static checker can't verify a plain `object` is callable


class StockPublisher:  # => holds ONLY a reference to EventBroker -- no Observer import anywhere
    def __init__(self, broker: EventBroker) -> None:  # => the constructor
        self._broker: EventBroker = broker  # => the ONLY collaborator type this class knows

    def set_price(self, price: float) -> None:  # => defines the set_price() method
        self._broker.publish("stock.price", price)  # => the publisher names a STRING topic, never a subscriber type


direct_subject: StockSubject = StockSubject()  # => constructs direct_subject
logger: PriceLogger = PriceLogger()  # => constructs logger
direct_subject.attach(logger)  # => the Subject holds a TYPED reference to this exact Observer
direct_subject.set_price(101.5)  # => notifies through the direct, typed reference
print(logger.history)  # => the direct observer received the update
# => Output: [101.5]

broker: EventBroker = EventBroker()  # => constructs broker
received: list[float] = []  # => a plain list, not required to satisfy any Observer interface
broker.subscribe("stock.price", received.append)  # => subscribes a PLAIN method, no interface at all
publisher: StockPublisher = StockPublisher(broker)  # => the publisher never imports Observer
publisher.set_price(202.5)  # => routed entirely through string-keyed topics
print(received)  # => the pub/sub subscriber received the update too, with NO shared base class
# => Output: [202.5]
# => `StockPublisher` never imports or references any concrete subscriber type -- only `EventBroker`
