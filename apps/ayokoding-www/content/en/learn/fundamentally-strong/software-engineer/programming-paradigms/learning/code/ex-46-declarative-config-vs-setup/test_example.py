"""Example 46: pytest verification for Declarative Config vs Setup."""

from example import Server, build_via_declared_spec, build_via_imperative_setup


def test_both_construction_styles_produce_an_equal_object() -> None:
    imperative = build_via_imperative_setup()  # => step-by-step mutation
    declared = build_via_declared_spec({"host": "api.example.com", "port": 443, "routes": ["/health", "/users"]})
    assert imperative == declared  # => dataclass structural equality


def test_declared_spec_with_different_values_builds_a_different_server() -> None:
    server = build_via_declared_spec({"host": "other.example.com", "port": 80, "routes": []})
    assert server == Server(host="other.example.com", port=80, routes=[])  # => matches the given spec exactly


# => Run: pytest -- Output: 2 passed
