"""Example 43: A Worker's Exception Is Stored, Then RE-RAISED by `.result()`."""

from concurrent.futures import Future, ThreadPoolExecutor  # => co-23, co-25: Futures carry exceptions too


class InsufficientFundsError(Exception):  # => a domain-specific exception, to show it's preserved EXACTLY
    """Raised by `risky_withdrawal` when the requested amount exceeds the balance."""


def risky_withdrawal(balance: int, amount: int) -> int:  # => the worker function that may fail
    if amount > balance:  # => the failure condition this example deliberately triggers
        raise InsufficientFundsError(f"cannot withdraw {amount} from balance {balance}")  # => raised INSIDE the worker thread
    return balance - amount  # => the success path -- only reached when the withdrawal is valid


if __name__ == "__main__":  # => module entry point
    with ThreadPoolExecutor(max_workers=2) as pool:  # => a pool with 2 worker threads
        good_future: Future[int] = pool.submit(risky_withdrawal, 100, 30)  # => a withdrawal that SHOULD succeed
        bad_future: Future[int] = pool.submit(risky_withdrawal, 100, 500)  # => a withdrawal that SHOULD fail

        good_result = good_future.result()  # => blocks until done, then returns the plain int -- no exception here
        print(f"good_result={good_result}")  # => Output: good_result=70

        raised: Exception | None = None  # => raised: captures whatever .result() throws, for inspection below
        try:
            bad_future.result()  # => submit() NEVER raises -- the exception is captured INSIDE the Future instead
        except InsufficientFundsError as exc:  # => .result() is where a stored exception gets RE-RAISED
            raised = exc  # => saves the caught exception so the assertions below can inspect it

    print(f"raised={raised!r}")  # => Output: raised=InsufficientFundsError('cannot withdraw 500 from balance 100')

    # => `submit()` never raises directly, even if the worker function will eventually fail -- the
    # => worker runs on a DIFFERENT thread, and an exception there can't unwind the caller's stack in
    # => real time. Instead, `ThreadPoolExecutor` CAPTURES the exception inside the Future object, and
    # => `.result()` is the point where it gets RE-RAISED, with its original type and message intact,
    # => on whichever thread calls `.result()` -- exactly as if it had been raised there directly.
    assert raised is not None  # => confirms .result() DID raise, rather than silently swallowing the error
    assert isinstance(raised, InsufficientFundsError)  # => confirms the ORIGINAL exception TYPE is preserved
    assert "500" in str(raised)  # => confirms the original MESSAGE survived the trip through the Future
    print("ex-43 OK")  # => Output: ex-43 OK
