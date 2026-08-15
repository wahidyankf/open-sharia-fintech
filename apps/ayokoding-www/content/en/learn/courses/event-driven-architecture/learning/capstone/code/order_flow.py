"""A self-contained local-broker capstone for the Event-Driven Architecture course."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Fact:
    id: str
    kind: str
    order_id: str


@dataclass
class OrderFlow:
    events: list[Fact] = field(default_factory=list)
    outbox: list[Fact] = field(default_factory=list)
    read_model: dict[str, str] = field(default_factory=dict)
    processed: set[str] = field(default_factory=set)
    published: list[Fact] = field(default_factory=list)
    dead_letters: list[Fact] = field(default_factory=list)
    completed_steps: list[str] = field(default_factory=list)
    compensations: list[str] = field(default_factory=list)

    def place(self, order_id: str) -> Fact:
        fact = Fact(f"placed:{order_id}", "OrderPlaced", order_id)
        self.events.append(fact)
        self.outbox.append(fact)
        return fact

    def relay(self) -> None:
        for fact in list(self.outbox):
            self.published.append(fact)
            self.outbox.remove(fact)

    def consume(self, fact: Fact, poison: bool = False) -> bool:
        if poison:
            self.dead_letters.append(fact)
            return False
        if fact.id in self.processed:
            return False
        self.processed.add(fact.id)
        self.read_model[fact.order_id] = "placed"
        return True

    def replay(self) -> dict[str, str]:
        state: dict[str, str] = {}
        for fact in self.events:
            if fact.kind == "OrderPlaced":
                state[fact.order_id] = "placed"
        return state

    def saga(self, payment_succeeds: bool) -> bool:
        self.completed_steps.append("reserve-inventory")
        if payment_succeeds:
            self.completed_steps.append("capture-payment")
            return True
        self.compensations.append("release-inventory")
        return False


def demo() -> None:
    flow = OrderFlow()
    event = flow.place("o-1")
    flow.relay()
    flow.consume(event)
    flow.consume(
        event
    )  # => deliberate redelivery; idempotency keeps one projection effect
    flow.saga(payment_succeeds=False)
    poison = Fact("poison:o-2", "OrderPlaced", "o-2")
    flow.consume(poison, poison=True)
    print(flow.replay())
    print(flow.read_model)
    print(flow.compensations)
    print([fact.id for fact in flow.dead_letters])


if __name__ == "__main__":
    demo()
