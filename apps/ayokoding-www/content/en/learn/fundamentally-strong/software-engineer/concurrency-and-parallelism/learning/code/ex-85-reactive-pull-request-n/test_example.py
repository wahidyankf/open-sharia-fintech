"""Example 85: pytest verification for Reactive Pull -- request(n) Bounds Emission."""

from example import SOURCE_ITEMS, DemandPublisher, DemandSubscriber


def test_no_item_is_emitted_before_any_demand_is_requested() -> None:
    publisher = DemandPublisher(SOURCE_ITEMS)
    subscriber = DemandSubscriber()
    publisher.subscribe(subscriber)  # => subscribing alone must not push anything
    assert subscriber.received == []  # => zero demand so far -- zero items delivered


def test_exactly_n_items_arrive_per_request_and_no_more() -> None:
    publisher = DemandPublisher(SOURCE_ITEMS)
    subscriber = DemandSubscriber()
    subscription = publisher.subscribe(subscriber)
    subscription.request(4)  # => ask for exactly 4
    assert subscriber.received == [0, 1, 2, 3]  # => exactly 4 delivered -- never more than outstanding demand
    assert subscriber.completed is False  # => 6 items remain -- the source is not exhausted yet


def test_completion_fires_exactly_once_when_demand_exhausts_the_source() -> None:
    publisher = DemandPublisher(SOURCE_ITEMS)
    subscriber = DemandSubscriber()
    subscription = publisher.subscribe(subscriber)
    subscription.request(len(SOURCE_ITEMS))  # => request the ENTIRE backlog in one shot
    assert subscriber.received == SOURCE_ITEMS  # => every item delivered, in order
    assert subscriber.completed is True  # => the source correctly signalled it has nothing left
    subscription.request(50)  # => a late over-request must be a harmless no-op, not a crash or a re-emit
    assert subscriber.received == SOURCE_ITEMS  # => unchanged -- no phantom items appear after completion


# => Run: pytest -- Output: 3 passed
