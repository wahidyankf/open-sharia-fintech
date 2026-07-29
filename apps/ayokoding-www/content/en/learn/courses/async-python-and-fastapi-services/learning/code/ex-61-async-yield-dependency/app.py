"""Example 61: An Async Yield Dependency with Cleanup.

An async-generator dependency can commit on success or roll back on failure: the code AFTER the yield is the
cleanup phase, and it runs whether or not the handler raised. Run: uvicorn app:app --port 8000. (co-15)
"""

from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException  # => DI + errors (co-15, co-17)


class Tx:  # => a stand-in for a transaction handle
    def __init__(self) -> None:
        self.committed = False  # => not yet committed

    async def commit(self) -> None:  # => persist the work
        self.committed = True  # => mark committed

    async def rollback(self) -> None:  # => undo the work
        self.committed = False  # => mark rolled back


app = FastAPI()  # => the ASGI application uvicorn serves


async def get_tx() -> AsyncIterator[Tx]:  # => an async yield dependency (co-15)
    tx = Tx()  # => START a transaction before the handler runs
    try:
        yield tx  # => hand the live transaction to the handler
        await tx.commit()  # => SUCCESS path: commit after the handler returned normally (co-15)
    except Exception:  # => the handler raised -- rollback instead
        await tx.rollback()  # => FAILURE path: undo, then re-raise is optional (co-15)
        raise  # => re-raise so FastAPI still maps it to a response


@app.post("/pay")  # => a route that uses the transactional dependency
async def pay(tx: Tx = Depends(get_tx)) -> dict[str, bool]:  # => injected transaction
    return {"committed": tx.committed}  # => False here -- commit happens AFTER the return (co-14)


@app.get("/boom")  # => a route that raises, forcing a rollback
async def boom(tx: Tx = Depends(get_tx)) -> dict[str, str]:  # => injected transaction
    raise HTTPException(status_code=400, detail="forced failure")  # => triggers the rollback path (co-17)
