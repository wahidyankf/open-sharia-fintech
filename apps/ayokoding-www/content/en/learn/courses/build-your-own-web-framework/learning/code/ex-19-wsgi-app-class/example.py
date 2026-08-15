"""Example 19: callable WSGI class."""

from collections.abc import Callable, Iterable


class App:
    def __call__(
        self,
        environ: dict[str, object],
        start: Callable[[str, list[tuple[str, str]]], None],
    ) -> Iterable[bytes]:
        # => A callable object has the same server contract as a function.
        start("200 OK", [])
        return [b"class app"]


def main() -> None:
    # => Servers care about callability, not declaration style.
    print(b"".join(App()({}, lambda status, headers: None)).decode())


if __name__ == "__main__":
    main()
