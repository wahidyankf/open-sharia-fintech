"""Kata 8 -- A response_model that strips a secret field (co-14)."""

ALLOWED_OUT_FIELDS = {"name"}  # => the output model's allowed fields (co-14)


def filter_output(
    input_dict: dict[str, object],
) -> dict[str, object]:  # => mimics response_model filtering
    return {
        k: v for k, v in input_dict.items() if k in ALLOWED_OUT_FIELDS
    }  # => keep only allowed fields (co-14)


def main() -> None:
    internal = {
        "name": "widget",
        "secret": "cost-is-3.50",
    }  # => the internal object has a secret
    out = filter_output(internal)  # => the output model strips it
    print(out)  # => Output: {'name': 'widget'}
    assert out == {"name": "widget"}  # => secret never reaches the output (co-14)
    assert "secret" not in out


if __name__ == "__main__":
    main()
