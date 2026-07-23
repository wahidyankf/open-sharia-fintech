"""Example 33: State Machine -- Imperative."""

state = "locked"  # => MUTABLE GLOBAL: the turnstile's current state lives in one module-level box
events: list[str] = ["coin", "push", "push", "coin", "coin", "push"]  # => a sequence to replay


def handle(event: str) -> None:  # => mutates the global `state` directly, one transition-if at a time
    global state  # => explicit acknowledgement this function reaches outside itself
    if state == "locked" and event == "coin":  # => explicit transition-if #1
        state = "unlocked"  # => mutate in place
    elif state == "locked" and event == "push":  # => explicit transition-if #2
        pass  # => pushing a locked turnstile does nothing -- state stays "locked"
    elif state == "unlocked" and event == "push":  # => explicit transition-if #3
        state = "locked"  # => mutate in place
    elif state == "unlocked" and event == "coin":  # => explicit transition-if #4
        pass  # => an extra coin on an already-unlocked turnstile changes nothing


history: list[str] = [state]  # => record the state after every event, starting with the initial one
for event in events:  # => replay every event against the mutable global
    handle(event)  # => each call may mutate `state`
    history.append(state)  # => record what it became

print(history)  # => locked -> unlocked (coin) -> locked (push) -> ... -> locked -> unlocked
# => Output: ['locked', 'unlocked', 'locked', 'locked', 'unlocked', 'unlocked', 'locked']
