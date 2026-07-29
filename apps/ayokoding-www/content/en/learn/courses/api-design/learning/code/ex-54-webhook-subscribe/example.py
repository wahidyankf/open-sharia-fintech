# pyright: strict
"""Example 54: Registering a Webhook Subscription. (co-33)

A webhook subscription is itself an API resource: a caller POSTs a target
URL and the event types it wants, and the API stores that subscription for
future OUTBOUND delivery -- the foundation Example 55's signing builds on.
"""

from dataclasses import dataclass, field  # => field: default_factory for the event-types list

SUBSCRIPTIONS: dict[int, dict[str, object]] = {}  # => co-33: id -> the stored subscription record
NEXT_ID = [1]  # => a mutable counter cell -- mints a fresh subscription id


@dataclass  # => co-33: what a caller submits to register a webhook
class WebhookSubscriptionRequest:  # => co-33: the two facts a subscription needs to be delivered
    url: str  # => the caller's OWN endpoint, where events will be delivered
    event_types: list[str] = field(default_factory=list[str])  # => which events this subscriber wants


def subscribe(request: WebhookSubscriptionRequest) -> dict[str, object]:  # => POST /webhooks
    subscription_id = NEXT_ID[0]  # => a fresh id for this subscription
    record: dict[str, object] = {  # => co-33: the full record, explicitly dict[str, object]
        "id": subscription_id,  # => the subscription's own id
        "url": request.url,  # => where events will be delivered
        "event_types": request.event_types,  # => which events this subscriber wants
    }  # => end of the record dict
    SUBSCRIPTIONS[subscription_id] = record  # => co-33: stored for future outbound delivery
    NEXT_ID[0] += 1  # => advances the counter for the NEXT subscription
    return record  # => echoes back what was just stored


SUBSCRIPTION_URL = "https://caller.example.com/hooks/articles"  # => the caller's own delivery endpoint
SUBSCRIPTION_EVENTS = ["article.created", "article.deleted"]  # => the two event types this caller wants
request = WebhookSubscriptionRequest(url=SUBSCRIPTION_URL, event_types=SUBSCRIPTION_EVENTS)  # => co-33 request
stored = subscribe(request)  # => co-33: registers the subscription
print(f"stored subscription: {stored}")  # => Output: id, url, and both event types, echoed back
print(f"total subscriptions: {len(SUBSCRIPTIONS)}")  # => Output: 1
# => the subscription is now stored server-side, ready for Example 55's signed delivery
