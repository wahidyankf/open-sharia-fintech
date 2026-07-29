"""Example 11: Type Checking Clean with pyright.

This module is fully type-annotated and pyright-clean (strict). Run: pyright example.py -> 0 errors. (co-09)
"""


def parse_port(raw: str) -> int:  # => every parameter AND the return are annotated (co-09)
    # => a ValueError narrows "bad input" to a precise, typed failure instead of an untyped crash
    value = int(raw)  # => may raise ValueError -- pyright knows value is int here
    if not (1 <= value <= 65535):  # => a valid TCP/UDP port range check
        raise ValueError(f"port out of range: {value}")  # => typed-domain rejection (no bare string fallback)
    return value  # => pyright confirms an int is returned on every path


def build_url(host: str, port_raw: str) -> str:  # => composes the typed parser into a larger function
    port = parse_port(port_raw)  # => pyright knows port is int -- no cast needed anywhere
    return f"http://{host}:{port}"  # => a fully-typed string result


if __name__ == "__main__":  # => run directly to confirm behaviour
    print(build_url("localhost", "8000"))  # => Output: http://localhost:8000
