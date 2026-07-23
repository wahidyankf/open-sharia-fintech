"""Example 42: Escalating a Support Ticket Through a Handler Chain."""

import abc  # => imports the abc module


class SupportHandler(abc.ABC):  # => one link in the chain -- each link decides FOR ITSELF
    def __init__(self) -> None:  # => the constructor
        self._next: "SupportHandler | None" = None  # => the NEXT link, set by set_next()

    def set_next(self, handler: "SupportHandler") -> "SupportHandler":  # => wires the chain
        self._next = handler  # => remembers who to escalate to
        return handler  # => returned so calls can be chained: a.set_next(b).set_next(c)

    def handle(self, severity: int) -> str:  # => defines the handle() method
        if self._can_handle(severity):  # => THIS link decides whether it owns the ticket
            return self._resolve(severity)  # => returns this value to the caller
        if self._next is not None:  # => not this link's job -- pass it further down the chain
            return self._next.handle(severity)  # => returns this value to the caller
        return "unhandled: no tier could resolve this ticket"  # => fell off the END of the chain

    @abc.abstractmethod
    def _can_handle(self, severity: int) -> bool:  # => no body -- required by every tier
        ...  # => the ellipsis stub -- concrete tiers below fill this in

    @abc.abstractmethod
    def _resolve(self, severity: int) -> str:  # => no body -- required by every tier
        ...  # => the ellipsis stub -- concrete tiers below fill this in


class L1Handler(SupportHandler):  # => handles only the LOWEST severities
    def _can_handle(self, severity: int) -> bool:  # => defines the _can_handle() method
        return severity <= 1  # => returns this value to the caller

    def _resolve(self, severity: int) -> str:  # => defines the _resolve() method
        return "resolved at L1"  # => returns this value to the caller


class L2Handler(SupportHandler):  # => handles the NEXT band of severities
    def _can_handle(self, severity: int) -> bool:  # => defines the _can_handle() method
        return severity <= 3  # => returns this value to the caller

    def _resolve(self, severity: int) -> str:  # => defines the _resolve() method
        return "resolved at L2"  # => returns this value to the caller


class L3Handler(SupportHandler):  # => the LAST link -- handles everything remaining
    def _can_handle(self, severity: int) -> bool:  # => defines the _can_handle() method
        return severity <= 5  # => returns this value to the caller

    def _resolve(self, severity: int) -> str:  # => defines the _resolve() method
        return "resolved at L3"  # => returns this value to the caller


l1: L1Handler = L1Handler()  # => constructs l1
l2: L2Handler = L2Handler()  # => constructs l2
l3: L3Handler = L3Handler()  # => constructs l3
l1.set_next(l2).set_next(l3)  # => wires L1 -> L2 -> L3, chained in one expression

print(l1.handle(1))  # => severity 1 -- L1 can handle it directly, no escalation needed
# => Output: resolved at L1
print(l1.handle(2))  # => severity 2 -- too high for L1, ESCALATES to L2 automatically
# => Output: resolved at L2
print(l1.handle(9))  # => severity 9 -- too high for every tier, falls off the end
# => Output: unhandled: no tier could resolve this ticket
# => An unhandled ticket automatically escalates to the NEXT handler, with no caller-side branching
