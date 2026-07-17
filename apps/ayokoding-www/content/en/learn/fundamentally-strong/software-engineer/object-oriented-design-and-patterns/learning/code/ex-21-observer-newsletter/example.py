"""Example 21: Observer: Notify Subscribers on Publish."""  # => module docstring

from typing import Callable  # => Callable types each subscriber this newsletter holds


class Newsletter:  # => the SUBJECT -- notifies subscribers, never inspects who they are
    def __init__(self) -> None:  # => the constructor
        self._subscribers: list[Callable[[str], None]] = []  # => the growing subscriber list

    def subscribe(  # => the registration method, spread across lines
        self,  # => the Newsletter instance itself
        handler: Callable[[str], None],
        # => subscribe() is NEVER edited to support a new kind of subscriber
    ) -> None:  # => defines the subscribe() method
        self._subscribers.append(handler)  # => the ONLY line that grows the list

    def publish(self, headline: str) -> None:  # => defines the publish() method
        for handler in self._subscribers:  # => notifies EVERY subscriber, in order
            handler(headline)  # => the subject never knows what a handler does with it


received: list[str] = []  # => a plain list one subscriber will append into
urgent: list[str] = []  # => a SECOND, independent list a different subscriber appends into


def log_subscriber(headline: str) -> None:  # => the FIRST subscriber, added via subscribe()
    received.append(headline)  # => records every headline this subscriber sees


def urgent_subscriber(headline: str) -> None:  # => a SECOND subscriber, zero edits to Newsletter
    if "URGENT" in headline:  # => this subscriber filters on its own terms
        urgent.append(headline)  # => only records headlines it cares about


newsletter: Newsletter = Newsletter()  # => constructs newsletter
newsletter.subscribe(log_subscriber)  # => registers subscriber one
newsletter.subscribe(urgent_subscriber)  # => registers subscriber two, same method call

newsletter.publish("Weekly digest")  # => both subscribers react, publish() never branches
newsletter.publish("URGENT: outage")  # => both subscribers react again, differently

print(received, urgent)  # => confirms both subscribers independently received events
# => Output: ['Weekly digest', 'URGENT: outage'] ['URGENT: outage']
# => Adding a third subscriber is one more `newsletter.subscribe(...)` call -- `publish()` never changes
