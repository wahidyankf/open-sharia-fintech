processed: set[str] = set()
effects: list[str] = []


def consume(message_id: str, body: str) -> None:
    # The processed ID makes a redelivery detectable before the side effect.
    if message_id in processed:
        return
    processed.add(message_id)
    # A production implementation persists this record with the effect.
    effects.append(body)


consume("m-1", "bill-account")
consume("m-1", "bill-account")
assert effects == ["bill-account"]
print(effects)
