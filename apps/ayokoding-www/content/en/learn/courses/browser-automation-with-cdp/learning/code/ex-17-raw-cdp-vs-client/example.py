"""Example 17: raw CDP JSON and a thin-client call have the same contract."""

import json  # => CDP's wire format is JSON, so compare serializable command values first.

# => The raw form states the id, domain method, and parameters explicitly.
raw_command = {
    "id": 7,
    "method": "Page.navigate",
    "params": {"url": "https://fixture.test/"},
}
# => A thin client may hide JSON construction, but it must preserve the same observable method and URL.
client_call = ("Page.navigate", "https://fixture.test/")
# => Compare contract data rather than timing or a live browser side effect.
assert (raw_command["method"], raw_command["params"]["url"]) == client_call
# => Output proves both approaches describe the same navigation request.
print(json.dumps(raw_command, sort_keys=True))
