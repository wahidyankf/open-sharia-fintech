"""Example 85: Reactive Pull -- a Subscriber's request(n) Bounds How Much the Producer Emits."""

# => co-29, co-32: this is the "reactive-pull" inversion of push -- the SOURCE stays silent until
# => the SINK asks for more. HAND-ROLLED (reactivex has no built-in demand/backpressure API).


class DemandSubscriber:  # => the SINK -- it never asks the producer for anything directly, only via a Subscription
    """Tracks every value it received, so a test can assert exactly what arrived and when."""

    def __init__(self) -> None:  # => a fresh subscriber starts with nothing received and no completion signal
        self.received: list[int] = []  # => received: every value pushed to `on_next`, in arrival order
        self.completed = False  # => completed: flips True once the source has no more items to give

    def on_next(self, value: int) -> None:  # => called by the producer, never by the subscriber itself
        self.received.append(value)  # => a value arrived -- this ONLY happens in response to `request(n)`

    def on_complete(self) -> None:  # => the terminal signal that says "nothing more is ever coming"
        self.completed = True  # => the producer has exhausted its items; no further `on_next` will follow


class DemandSubscription:  # => the PULL HANDLE -- the only way the subscriber can ask for more items
    """The handshake object: the subscriber calls `request(n)` on THIS to pull more items."""

    def __init__(self, subscriber: DemandSubscriber, items: list[int]) -> None:  # => wires the pair together
        self.subscriber = subscriber  # => subscriber: who to notify when demand is satisfied
        self.items = items  # => items: the full backlog the producer COULD emit, if asked
        self.index = 0  # => index: how far into `items` production has progressed so far
        self.demand = 0  # => demand: outstanding "please send me N more" requests, not yet fulfilled
        self.done = False  # => done: guards against emitting `on_complete` more than once

    def request(self, n: int) -> None:  # => the ONE method the subscriber is allowed to call to get data
        if self.done:  # => the stream already finished -- a late `request` is simply a no-op
            return  # => bail out immediately -- no items, no re-firing of on_complete
        self.demand += n  # => ADD to any existing demand -- requests are cumulative, not a reset
        self._drain()  # => immediately try to satisfy as much of the new demand as possible

    def _drain(self) -> None:  # => internal helper -- never called from outside this class
        while self.demand > 0 and self.index < len(self.items):  # => stop the INSTANT demand hits zero
            value = self.items[self.index]  # => the next undelivered item, in order
            self.index += 1  # => advance the production cursor -- this item is now spoken for
            self.demand -= 1  # => consume exactly one unit of outstanding demand per item emitted
            self.subscriber.on_next(value)  # => push -- but ONLY because demand authorized it
        if self.index >= len(self.items) and not self.done:  # => every item has been emitted, exactly once
            self.done = True  # => flip the guard before notifying, so a re-entrant `request` can't double-fire
            self.subscriber.on_complete()  # => tell the subscriber the source is exhausted


class DemandPublisher:  # => the SOURCE -- deliberately dumb, it holds data but never pushes it uninvited
    """A cold source that emits NOTHING until a subscriber explicitly pulls via `request(n)`."""

    def __init__(self, items: list[int]) -> None:  # => a publisher is just a fixed, immutable backlog
        self.items = items  # => the fixed backlog this publisher can hand out on demand

    def subscribe(self, subscriber: DemandSubscriber) -> DemandSubscription:  # => creates the pull handle
        return DemandSubscription(subscriber, self.items)  # => wiring only -- zero items pushed yet


SOURCE_ITEMS = list(range(10))  # => 10 items total: 0..9


if __name__ == "__main__":  # => module entry point
    publisher = DemandPublisher(SOURCE_ITEMS)  # => a publisher holding all 10 items, none delivered yet
    subscriber = DemandSubscriber()  # => a fresh subscriber -- received=[] until it asks for something
    subscription = publisher.subscribe(subscriber)  # => subscribing alone triggers ZERO emissions
    print(f"after subscribe: received={subscriber.received}")  # => Output: after subscribe: received=[]

    subscription.request(3)  # => pull exactly 3 items
    print(f"after request(3): received={subscriber.received}")  # => Output: after request(3): received=[0, 1, 2]

    subscription.request(4)  # => pull 4 more -- cumulative with what already happened, not a fresh window
    print(f"after request(4): received={subscriber.received}")  # => Output: received=[0, 1, 2, 3, 4, 5, 6]

    subscription.request(3)  # => only 3 items remain (7, 8, 9) -- this exactly exhausts the source
    print(f"after request(3): received={subscriber.received} completed={subscriber.completed}")  # => Output: completed=True

    subscription.request(100)  # => a late, oversized request after completion -- must be a harmless no-op
    print(f"after late request(100): received={subscriber.received}")  # => Output: unchanged, still 10 items

    # => The subscriber is the ONE THING driving emission: nothing crosses the boundary until the
    # => sink says how much it can handle right now. This is the exact inverse of a normal push
    # => Observable (co-30), and it's how real backpressure protocols (Reactive Streams / JDK
    # => `Flow`, RxJava's `request(n)`) prevent a fast producer from ever overwhelming a slow
    # => consumer's buffer -- the producer is STRUCTURALLY incapable of sending more than was asked.
    assert subscriber.received == list(range(10))  # => all 10 items arrived, but ONLY across three requests
    assert subscriber.completed is True  # => the source correctly signalled exhaustion exactly once
    print("ex-85 OK")  # => Output: ex-85 OK
