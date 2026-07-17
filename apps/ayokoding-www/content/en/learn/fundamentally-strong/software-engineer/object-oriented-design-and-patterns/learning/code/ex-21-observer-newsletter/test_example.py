"""Example 21: pytest verification for Observer: Notify Subscribers on Publish."""

from example import Newsletter


def test_every_subscriber_is_notified_on_publish() -> None:
    received: list[str] = []
    newsletter: Newsletter = Newsletter()
    newsletter.subscribe(lambda headline: received.append(headline))  # => one subscriber
    newsletter.publish("hello")
    assert received == ["hello"]  # => the subscriber genuinely fired


def test_a_new_subscriber_needs_zero_edits_to_newsletter() -> None:
    # => registers a SECOND subscriber here, without touching Newsletter's source at all
    seen_by_second: list[str] = []
    newsletter: Newsletter = Newsletter()
    newsletter.subscribe(lambda headline: seen_by_second.append(headline.upper()))
    newsletter.publish("breaking news")
    assert seen_by_second == ["BREAKING NEWS"]  # => a brand-new behavior, zero edits above


# => Run: pytest -- Output: 2 passed
