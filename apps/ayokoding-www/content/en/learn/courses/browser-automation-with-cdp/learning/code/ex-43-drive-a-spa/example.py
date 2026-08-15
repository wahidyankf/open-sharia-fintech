"""Example 43: drive a client-side fixture flow with state-based readiness."""

# => Route state replaces a fixed sleep as the readiness condition for the next SPA step.
state = {"route": "/", "heading": "Home"}
# => A modeled click changes route and rendered heading together.
state.update(route="/report", heading="Report")
# => Assert the user-visible state after the client-side transition.
assert state == {"route": "/report", "heading": "Report"}
# => Output names the SPA state that became ready.
print(state["heading"])
