"""Example 55: pytest verification for Direct Observer vs a Pub/Sub Broker."""

import inspect

from example import EventBroker, PriceLogger, StockPublisher, StockSubject


def test_direct_observer_notifies_the_attached_observer() -> None:
    subject: StockSubject = StockSubject()
    logger: PriceLogger = PriceLogger()
    subject.attach(logger)
    subject.set_price(101.5)
    assert logger.history == [101.5]


def test_pubsub_publisher_notifies_a_plain_subscriber_callable() -> None:
    broker: EventBroker = EventBroker()
    received: list[float] = []
    broker.subscribe("stock.price", received.append)  # => no shared base class required
    StockPublisher(broker).set_price(202.5)
    assert received == [202.5]


def test_pubsub_publisher_never_references_the_observer_type() -> None:
    # => the added decoupling: StockPublisher's constructor signature names only
    # => EventBroker, never Observer -- unlike StockSubject.attach(), which requires it
    params = inspect.signature(StockPublisher.__init__).parameters
    annotations = [str(p.annotation) for p in params.values()]
    assert not any("Observer" in a for a in annotations)  # => StockPublisher's signature never names Observer
    attach_params = inspect.signature(StockSubject.attach).parameters
    attach_annotations = [str(p.annotation) for p in attach_params.values()]
    assert any("Observer" in a for a in attach_annotations)  # => StockSubject.attach() DOES require it directly


# => Run: pytest -- Output: 3 passed
