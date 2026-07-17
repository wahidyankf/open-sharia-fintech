"""Example 42: A Parameterized @retry(3) Decorator."""

from typing import Callable  # => Callable types every layer of this decorator factory

attempt_log: list[
    int
] = []  # => records which attempt number ran, for verification below


def retry(
    times: int,
) -> Callable[[Callable[[], str]], Callable[[], str]]:  # => a decorator FACTORY
    def decorator(
        fn: Callable[[], str],
    ) -> Callable[[], str]:  # => the ACTUAL decorator, closes over times
        def wrapper() -> str:  # => the actual retry loop lives here
            last_error: Exception | None = (
                None  # => remembers the most recent failure, if any
            )
            for attempt in range(
                1, times + 1
            ):  # => tries up to `times` times, closed over from retry()
                attempt_log.append(attempt)  # => logs every attempt, successful or not
                try:  # => attempts ONE call to the wrapped function
                    return fn()  # => success: return immediately, no further attempts
                except (
                    ValueError
                ) as exc:  # => a failed attempt -- remember it and try again
                    last_error = (
                        exc  # => remembers the failure so it can be re-raised later
                    )
            raise last_error  # type: ignore[misc]  # => every attempt failed -- re-raise the last error

        return wrapper  # => decorator itself returns the retry-wrapped function

    return decorator  # => retry(times) itself returns the decorator


calls_before_success = 0  # => simulates a flaky operation succeeding on its 3rd attempt


@retry(
    3
)  # => equivalent to: flaky = retry(3)(flaky) -- retry(3) runs FIRST, returns a decorator
def flaky() -> str:  # => the function actually being retried
    global calls_before_success  # => declares intent to mutate the MODULE-level counter
    calls_before_success += 1  # => tracks how many times this call has been attempted
    if calls_before_success < 3:  # => fails on attempts 1 and 2
        raise ValueError(
            "not yet"
        )  # => simulates a transient failure on early attempts
    return "ok"  # => succeeds on attempt 3


result = flaky()  # => retries internally until success, or until times is exhausted

# => a decorator factory is a function that RETURNS a decorator, one extra layer
print(result)  # => Output: ok
print(attempt_log)  # => Output: [1, 2, 3] -- three attempts were logged before success
