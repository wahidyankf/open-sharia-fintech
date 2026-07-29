"""Kata 6 -- Map a domain exception to an HTTP-like response (co-17)."""


class NotFound(Exception):  # => a domain error (co-17)
    pass


class Conflict(Exception):  # => another domain error
    pass


def dispatch(
    handler, exc_map: dict[type[Exception], tuple[int, str]]
):  # => runs handler, maps failures (co-17)
    try:
        return 200, handler()  # => the success path
    except Exception as exc:  # => a domain error raised by the handler
        for exc_type, mapping in exc_map.items():  # => find the mapped class
            if isinstance(exc, exc_type):
                return mapping  # => the mapped (status, body)
        raise  # => unmapped -> re-raise (co-17)


def read_missing():  # => raises NotFound
    raise NotFound()


def create_conflict():  # => raises Conflict
    raise Conflict()


def main() -> None:
    mapping = {
        NotFound: (404, "not found"),
        Conflict: (409, "conflict"),
    }  # => the central mapping (co-17)
    print(dispatch(read_missing, mapping))  # => Output: (404, 'not found')
    print(dispatch(create_conflict, mapping))  # => Output: (409, 'conflict')
    assert dispatch(read_missing, mapping) == (404, "not found")


if __name__ == "__main__":
    main()
