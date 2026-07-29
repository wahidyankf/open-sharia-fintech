"""Kata 10 -- Load typed config from a dict (mimicking pydantic-settings) (co-24)."""

DEFAULTS: dict[str, object] = {"env": "dev", "port": 8000}  # => co-24: typed defaults
TYPES: dict[str, type] = {"env": str, "port": int}  # => the expected type per field


def load_settings(
    raw: dict[str, object],
) -> dict[str, object]:  # => mimics pydantic-settings (co-24)
    out: dict[str, object] = dict(DEFAULTS)  # => start from defaults
    for key, value in raw.items():  # => apply overrides
        if key in TYPES and not isinstance(
            value, TYPES[key]
        ):  # => wrong type -> fail fast (co-24)
            raise ValueError(
                f"{key} must be {TYPES[key].__name__}, got {type(value).__name__}"
            )
        out[key] = value  # => accepted override
    return out  # => resolved config


def main() -> None:
    ok = load_settings({"port": 9000})  # => override applies, env stays default
    print(ok)  # => Output: {'env': 'dev', 'port': 9000}
    assert ok["port"] == 9000
    raised = False
    try:
        load_settings({"port": "not-an-int"})  # => wrong type -> ValueError (co-24)
    except ValueError:
        raised = True
    print(raised)  # => Output: True
    assert raised is True


if __name__ == "__main__":
    main()
