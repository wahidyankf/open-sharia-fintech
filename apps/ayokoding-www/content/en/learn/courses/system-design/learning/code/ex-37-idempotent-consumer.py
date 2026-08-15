# => Initialize or update deterministic state used by this demonstration.
processed: set[str] = set()
# => Initialize or update deterministic state used by this demonstration.
effects: list[str] = []


# => Isolate the operation so its observable behavior can be checked.
def consume(message_id: str, body: str) -> None:
    # The processed ID makes a redelivery detectable before the side effect.
    # => Choose the branch that models this design condition.
    if message_id in processed:
        # => Initialize or update deterministic state used by this demonstration.
        return
    # => Initialize or update deterministic state used by this demonstration.
    processed.add(message_id)
    # A production implementation persists this record with the effect.
    # => Initialize or update deterministic state used by this demonstration.
    effects.append(body)


# => Initialize or update deterministic state used by this demonstration.
consume("m-1", "bill-account")
# => Initialize or update deterministic state used by this demonstration.
consume("m-1", "bill-account")
# => Check the promised observable behavior of the demonstration.
assert effects == ["bill-account"]
# => Emit the final observable state for a direct run.
print(effects)
