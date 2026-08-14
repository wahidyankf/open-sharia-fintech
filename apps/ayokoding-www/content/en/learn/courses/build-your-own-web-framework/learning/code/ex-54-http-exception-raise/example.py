"""Example 54: intentional HTTP exception."""


class HTTPException(Exception):
    # => The exception carries protocol intent to the outer error boundary.
    def __init__(self, status: int) -> None:
        self.status = status


def main() -> None:
    # => A handler may stop immediately with an intentional failure.
    try:
        raise HTTPException(404)
    except HTTPException as error:
        print(error.status)


if __name__ == "__main__":
    main()
