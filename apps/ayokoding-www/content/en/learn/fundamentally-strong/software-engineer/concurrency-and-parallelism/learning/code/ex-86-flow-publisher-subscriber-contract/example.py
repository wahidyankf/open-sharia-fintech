"""Example 86: A java.util.concurrent.Flow-Style Contract, Hand-Rolled in Python."""

# => co-29: the Reactive Streams spec's four interfaces (Publisher/Subscriber/Subscription/Processor)
# => were adopted into the JDK as `java.util.concurrent.Flow` (Java 9). This mirrors that CONTRACT --
# => on_subscribe exactly once, then request-driven on_next*, then exactly one terminal signal
# => (on_complete XOR on_error), never on_next after a terminal. HAND-ROLLED (no reactivex API here).


class ContractViolation(RuntimeError):  # => a distinct exception type -- never conflated with a normal ValueError
    """Raised the instant a Subscriber method is invoked out of the Flow-contract order."""


class RecordingSubscriber:  # => the SINK -- both obeys the contract AND polices it against itself
    """A Subscriber that both fulfils the contract AND actively enforces it against itself."""

    def __init__(self) -> None:  # => a fresh subscriber starts unsubscribed, unterminated, with an empty log
        self.log: list[str] = []  # => log: every signal received, in the exact order it arrived
        self.subscribed = False  # => subscribed: True once on_subscribe has fired
        self.terminated = False  # => terminated: True once EITHER on_complete or on_error has fired
        self.subscription: "FlowSubscription | None" = None  # => the handle used to pull more items

    def on_subscribe(self, subscription: "FlowSubscription") -> None:  # => MUST be the first signal, ever
        if self.subscribed:  # => the contract says on_subscribe fires AT MOST once per subscriber
            raise ContractViolation("on_subscribe called more than once")  # => reject the second call outright
        self.subscribed = True  # => flip the guard before anything else can go wrong
        self.subscription = subscription  # => stash the handle so calling code can `request(n)` later
        self.log.append("subscribe")  # => record the signal for order verification

    def on_next(self, item: int) -> None:  # => called by the Subscription, never invoked directly by tests
        if not self.subscribed or self.terminated:  # => on_next must fall STRICTLY between subscribe and terminal
            raise ContractViolation("on_next called before subscribe or after a terminal signal")  # => illegal state
        self.log.append(f"next:{item}")  # => record exactly which value arrived and when

    def on_error(self, error: BaseException) -> None:  # => the FAILURE terminal signal
        if self.terminated:  # => a terminal signal must never follow another terminal signal
            raise ContractViolation("on_error called after a terminal signal already fired")  # => double-terminal is illegal
        self.terminated = True  # => flip BEFORE logging, so a re-entrant call can't slip through
        self.log.append(f"error:{error}")  # => record the failure, distinct from a normal completion

    def on_complete(self) -> None:  # => the SUCCESS terminal signal -- mutually exclusive with on_error
        if self.terminated:  # => same guard as on_error -- exactly one terminal signal, ever
            raise ContractViolation("on_complete called after a terminal signal already fired")  # => same illegal state
        self.terminated = True  # => flip before logging, matching on_error's ordering discipline
        self.log.append("complete")  # => record the clean-finish signal


class FlowSubscription:  # => the PULL HANDLE -- also owns the demand accounting from ex-85
    """Demand accounting: items only flow out in response to `request(n)`, exactly like ex-85."""

    def __init__(self, subscriber: RecordingSubscriber, items: list[int], fail_at: int | None) -> None:
        self.subscriber = subscriber  # => who to deliver on_next/on_error/on_complete to
        self.items = items  # => the full backlog available to emit
        self.fail_at = fail_at  # => optional index at which to simulate a producer-side failure
        self.index = 0  # => how far production has progressed
        self.demand = 0  # => outstanding, not-yet-fulfilled pull requests
        self.cancelled = False  # => True once `cancel()` has been called -- stops all further activity
        self.done = False  # => True once a terminal signal has been sent -- prevents a double-terminal

    def request(self, n: int) -> None:  # => the ONLY method that authorizes emission
        if self.cancelled or self.done:  # => a cancelled or finished subscription ignores further requests
            return  # => harmless no-op -- never crashes, never re-fires a terminal signal
        self.demand += n  # => demand accumulates across multiple `request` calls
        self._drain()  # => attempt to satisfy as much demand as the backlog (and failure point) allow

    def cancel(self) -> None:  # => lets a subscriber withdraw BEFORE the source finishes on its own
        self.cancelled = True  # => the subscriber withdraws interest -- no further signals will be sent

    def _drain(self) -> None:  # => internal push loop -- private to this class, never called externally
        while self.demand > 0 and self.index < len(self.items) and not self.cancelled:  # => stop at zero demand
            if self.fail_at is not None and self.index == self.fail_at:  # => simulate a producer-side error
                self.done = True  # => guard first, so the loop can never re-enter after this
                self.subscriber.on_error(ValueError(f"synthetic failure at index {self.index}"))  # => terminal
                return  # => on_error is TERMINAL -- no further on_next may follow, ever
            value = self.items[self.index]  # => the next undelivered item
            self.index += 1  # => advance production
            self.demand -= 1  # => consume one unit of demand per item pushed
            self.subscriber.on_next(value)  # => push -- authorized by outstanding demand, per the contract
        if self.index >= len(self.items) and not self.cancelled and not self.done:  # => backlog fully drained
            self.done = True  # => guard before notifying, matching the on_error path above
            self.subscriber.on_complete()  # => clean finish -- every item was delivered, nothing failed


class FlowPublisher:  # => the SOURCE -- optionally configured to fail at a specific index for testing
    """Wires a fresh Subscription to a Subscriber the instant subscribe() is called."""

    def __init__(self, items: list[int], fail_at: int | None = None) -> None:  # => a fixed backlog + failure mode
        self.items = items  # => the backlog this publisher can emit
        self.fail_at = fail_at  # => None means "always succeeds"; an int means "fail at this index"

    def subscribe(self, subscriber: RecordingSubscriber) -> FlowSubscription:  # => the ONLY Publisher method
        subscription = FlowSubscription(subscriber, self.items, self.fail_at)  # => build the pull handle first
        subscriber.on_subscribe(subscription)  # => on_subscribe fires FIRST, before any request is even possible
        return subscription  # => hand the handle back so the caller can start pulling via `request(n)`


if __name__ == "__main__":  # => module entry point
    happy_publisher = FlowPublisher([10, 20, 30])  # => a 3-item source, no failure configured
    happy_subscriber = RecordingSubscriber()  # => tracks the entire signal sequence for this run
    happy_subscription = happy_publisher.subscribe(happy_subscriber)  # => fires on_subscribe immediately
    print(f"after subscribe: log={happy_subscriber.log}")  # => Output: log=['subscribe']

    happy_subscription.request(2)  # => pull 2 -- demand-driven, exactly like ex-85
    happy_subscription.request(5)  # => pull the rest -- more than remains, which is fine, it just drains
    print(f"happy path log: {happy_subscriber.log}")  # => Output: ['subscribe','next:10','next:20','next:30','complete']

    failing_publisher = FlowPublisher([1, 2, 3, 4], fail_at=2)  # => this source WILL synthesize a failure
    failing_subscriber = RecordingSubscriber()  # => a separate subscriber for the error-path scenario
    failing_subscription = failing_publisher.subscribe(failing_subscriber)  # => fires on_subscribe for this pair
    failing_subscription.request(10)  # => ask for everything -- production stops at the synthetic failure
    print(f"error path log: {failing_subscriber.log}")  # => Output: ['subscribe','next:1','next:2','error:...']

    violation_caught = False  # => tracks whether the contract-violation guard actually fired
    try:  # => deliberately misuse the finished happy_subscriber to prove the guard works
        happy_subscriber.on_next(999)  # => illegal: on_next AFTER on_complete already fired above
    except ContractViolation:  # => this is the EXPECTED outcome -- the guard must reject it
        violation_caught = True  # => the self-enforcing guard correctly rejected the illegal call

    # => The contract has THREE non-negotiable shape rules, all enforced here BY THE SUBSCRIBER
    # => ITSELF rather than trusted to caller discipline: (1) on_subscribe fires exactly once and
    # => always first; (2) on_next only ever happens between subscribe and a terminal signal, and
    # => only in response to outstanding demand from request(n); (3) exactly one terminal signal
    # => (on_complete XOR on_error) ever fires, and nothing legally follows it. This is precisely
    # => what makes `java.util.concurrent.Flow` and Reactive Streams composable across unrelated
    # => libraries -- every implementation obeys the SAME ordering guarantees, so adapters between
    # => them never have to guess what state the other side is in.
    assert happy_subscriber.log == ["subscribe", "next:10", "next:20", "next:30", "complete"]  # => full happy sequence
    assert failing_subscriber.log == ["subscribe", "next:1", "next:2", "error:synthetic failure at index 2"]  # => stops at fail_at
    assert failing_subscriber.terminated is True  # => the error path correctly reached a terminal state
    assert violation_caught is True  # => the contract guard fired exactly when it should have
    print("ex-86 OK")  # => Output: ex-86 OK
