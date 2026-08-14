"""Example 51: dependency direction points toward domain policy."""

DOMAIN_IMPORTS: set[str] = set()  # => domain names no framework or database dependency
APPLICATION_IMPORTS = {"domain"}  # => application may coordinate domain types
INFRASTRUCTURE_IMPORTS = {"domain"}  # => adapters implement policy-owned ports

assert not DOMAIN_IMPORTS and "domain" in INFRASTRUCTURE_IMPORTS
