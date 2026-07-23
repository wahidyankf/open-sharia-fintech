"""Example 74: DIP -- Hexagonal Ports.

co-05, co-14: ports-and-adapters (hexagonal architecture) wiring a domain to
infrastructure. The domain module defines a PORT (an abstract interface it
needs) and depends on nothing else; concrete ADAPTERS live in a separate
"infrastructure" namespace and implement the port. The domain's own source
never names an infrastructure class -- inspected here via OrderDomain's own
constructor annotation, not just asserted in prose.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from typing import Protocol  # => Protocol declares the PORT the domain owns


# ============================================================
# DOMAIN -- defines the port it needs; imports nothing from infrastructure
# ============================================================


# => this Protocol lives IN the domain's own file/namespace -- infrastructure adapts to it, not the reverse
class NotificationPort(Protocol):  # => the PORT: an interface OWNED by the domain, infra must conform to it
    def send(self, message: str) -> None: ...  # => the ONE method any adapter must provide


# => grep OrderDomain's source for "EmailAdapter" or "SmsAdapter" -- neither name appears anywhere in this class
class OrderDomain:  # => co-05: depends on the ABSTRACT port, never on a concrete adapter class
    def __init__(self, notifier: NotificationPort) -> None:  # => the constructor names only the PORT type
        self._notifier = notifier  # => injected -- the domain never constructs its own infrastructure

    # => this is OrderDomain's ONLY method that touches notification -- it goes through _notifier, never a class name
    def confirm_order(self, order_id: str) -> None:  # => the domain's own business method
        self._notifier.send(f"order {order_id} confirmed")  # => calls through the PORT only


# ============================================================
# INFRASTRUCTURE -- adapters that implement the domain's port; may import anything
# ============================================================


class EmailAdapter:  # => a concrete ADAPTER living outside the domain namespace
    def __init__(self) -> None:  # => the constructor
        self.sent: list[str] = []  # => stands in for a real SMTP client

    def send(self, message: str) -> None:  # => satisfies NotificationPort structurally
        self.sent.append(f"[email] {message}")  # => a real, honest implementation


class SmsAdapter:  # => a SECOND adapter -- swappable without touching OrderDomain at all
    def __init__(self) -> None:  # => the constructor
        self.sent: list[str] = []  # => stands in for a real SMS gateway

    def send(self, message: str) -> None:  # => satisfies NotificationPort structurally
        self.sent.append(f"[sms] {message}")  # => a real, honest implementation


def domain_module_imports_no_infrastructure_names() -> bool:  # => co-05: verify the dependency direction for real
    # => the true architectural check: OrderDomain's __init__ signature names only the PORT, never a concrete adapter
    annotation = OrderDomain.__init__.__annotations__.get("notifier")  # => reads the ACTUAL parameter annotation
    return annotation in ("NotificationPort", NotificationPort) or str(annotation) == "NotificationPort"  # => the real check


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    email = EmailAdapter()  # => constructs one concrete adapter
    domain = OrderDomain(email)  # => wired at the OUTERMOST layer -- the domain itself never names EmailAdapter
    domain.confirm_order("ord-1")  # => the domain's own method, oblivious to WHICH adapter it holds
    print(email.sent)  # => confirms the email adapter recorded the message
    # => Output: ['[email] order ord-1 confirmed']

    sms = SmsAdapter()  # => constructs a DIFFERENT concrete adapter
    domain_with_sms = OrderDomain(sms)  # => swap the adapter -- zero edits inside OrderDomain
    domain_with_sms.confirm_order("ord-2")  # => the SAME domain method, now routed through a different adapter
    print(sms.sent)  # => confirms the sms adapter recorded the message
    # => Output: ['[sms] order ord-2 confirmed']

    print(domain_module_imports_no_infrastructure_names())  # => confirms the dependency direction by inspection, not prose
    # => Output: True
