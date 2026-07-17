"""Example 46: Declarative Config vs Setup."""

from dataclasses import dataclass, field  # => @dataclass generates __init__; field() gives a fresh list


@dataclass  # => auto-generates Server's __init__ from the three fields below
class Server:  # => the object both styles below must end up constructing, identically
    host: str = "localhost"  # => default value, overridden by both build functions below
    port: int = 8080  # => default value, overridden by both build functions below
    routes: list[str] = field(default_factory=list[str])  # => default: a fresh empty list per instance


def build_via_imperative_setup() -> Server:  # => HOW: step-by-step mutation after construction
    server = Server()  # => start from the defaults
    server.host = "api.example.com"  # => step 1: mutate host
    server.port = 443  # => step 2: mutate port
    server.routes.append("/health")  # => step 3: mutate routes
    server.routes.append("/users")  # => step 4: mutate routes again
    return server  # => the fully-mutated object


DECLARED_SPEC: dict[str, object] = {  # => WHAT: the desired final shape, stated as data up front
    "host": "api.example.com",  # => same value the imperative version reaches via mutation
    "port": 443,  # => same value the imperative version reaches via mutation
    "routes": ["/health", "/users"],  # => same value the imperative version reaches via two .append() calls
}  # => closes the declared spec -- one value, no steps


def build_via_declared_spec(spec: dict[str, object]) -> Server:  # => construct directly FROM the spec
    return Server(host=str(spec["host"]), port=int(spec["port"]), routes=list(spec["routes"]))  # => reads the whole desired shape from spec in one call  # type: ignore[arg-type]
    # => one call, reading the entire desired shape from a single declared value


imperative_server = build_via_imperative_setup()  # => run the step-by-step version
declarative_server = build_via_declared_spec(DECLARED_SPEC)  # => run the declared-spec version

print(imperative_server)  # => both objects must be field-for-field equal
# => Output: Server(host='api.example.com', port=443, routes=['/health', '/users'])
print(imperative_server == declarative_server)  # => dataclasses compare structurally by default
# => Output: True
