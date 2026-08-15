# Namespaces retain each provider's authority boundary.
providers = {"fs.read": "note", "shell.status": "ok", "browser.title": "Fixture"}
# Composition reads one result from every local provider.
result = tuple(providers.values())
# Each result remains attributed by its key.
assert result == ("note", "ok", "Fixture")
# Print the composed local result.
print(result)
