"""Example 73: expose a narrow navigate tool rather than arbitrary execution."""

# => The schema permits one operation and a fixture URL, not arbitrary JavaScript.
tool = {"name": "navigate_fixture", "parameters": {"url": "https://fixture.test/docs"}}
# => A least-privilege contract communicates its exact allowed capability.
allowed = tool["name"] == "navigate_fixture" and tool["parameters"]["url"].startswith(
    "https://fixture.test/"
)
# => The assertion rejects an over-broad generic execute surface.
assert allowed is True
# => Output identifies the deliberately narrow tool.
print(tool["name"])
