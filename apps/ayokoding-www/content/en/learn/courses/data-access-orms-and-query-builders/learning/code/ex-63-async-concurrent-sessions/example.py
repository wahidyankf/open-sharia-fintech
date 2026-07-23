# pyright: strict
"""Example 63: asyncio.gather Over Independent Sessions -- Real Concurrent Queries."""

from __future__ import annotations

import asyncio  # => co-24: gather() is what actually runs the sessions concurrently
import os  # => reads connection settings from the environment
import time  # => wall-clock timing -- the measured evidence that this ran concurrently, not sequentially

from sqlalchemy import select, text  # => select() is identical in sync and async
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine  # => co-24: the async counterparts of Engine/Session
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

SQLA_URL: str = os.environ.get(  # => the SAME `+psycopg` URL string works for both sync and async engines
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-24: a plain mapped class -- concurrency here is about SESSIONS, not the mapping itself
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


async def reset_schema(engine: AsyncEngine) -> None:  # => an async reset helper -- `async with`, not `with`
    async with engine.begin() as conn:  # => `async with` -- awaits the connection AND the commit/rollback on exit
        await conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        await conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
        await conn.run_sync(Base.metadata.create_all)  # => run_sync() bridges Core's sync DDL onto the async connection


async def slow_query(engine: AsyncEngine, label: str) -> str:  # => co-24: EACH call opens its OWN session -- never shared across tasks
    async with AsyncSession(engine) as session:  # => a session is NOT safe to share between concurrent coroutines
        await session.execute(select(text("pg_sleep(0.2)")))  # => co-24: simulates a slow query -- 0.2s of server-side wait, per task
        result = await session.execute(select(Customer))  # => a real second round trip, so this is genuine query work, not just sleep
        _ = result.scalars().all()  # => reads the rows -- discarded, only the round trip timing matters here
    return label  # => identifies which of the concurrent tasks this is, once gather() resolves everything


async def main() -> None:  # => co-24: the async entry point -- everything below runs on the event loop asyncio.run() starts
    engine = create_async_engine(SQLA_URL, pool_size=5)  # => co-18 + co-24: pool must hold enough connections for ALL concurrent tasks
    await reset_schema(engine)  # => awaited -- schema setup happens before any query below runs

    async with AsyncSession(engine) as session:  # => a plain setup session -- seeds one row so the SELECT below has work to do
        session.add(Customer(name="Ada"))  # => a single seed row, just so the concurrent queries aren't hitting an empty table
        await session.commit()  # => commit() IS async -- it issues the actual INSERT over the network

    start = time.monotonic()  # => wall-clock start, right before the concurrent tasks launch
    # => co-24: a SINGLE event loop, no threads, no processes -- concurrency here comes purely from cooperative
    # => yielding at every `await`, which is exactly why a lazy load (Example 62) can't safely run implicitly
    labels = await asyncio.gather(  # => co-24: gather() runs all THREE tasks CONCURRENTLY on the one event loop, not one-by-one
        slow_query(engine, "task-a"),  # => co-24: each task gets its OWN AsyncSession -- sessions are never thread/task-shared
        slow_query(engine, "task-b"),  # => runs concurrently with task-a and task-c, not sequentially after them
        slow_query(engine, "task-c"),  # => the THIRD concurrent task, sharing the SAME pool but a DIFFERENT session
    )
    elapsed = time.monotonic() - start  # => co-24: total wall-clock time for all three 0.2s-sleep tasks TOGETHER

    # => co-18 + co-24: pool_size=5 comfortably covers 3 concurrent checkouts -- a pool sized too small would serialize
    # => tasks waiting on a free connection instead of genuinely overlapping their I/O (see Example 46, pool exhaustion)
    print(f"labels={sorted(labels)}")  # => Output: labels=['task-a', 'task-b', 'task-c']
    print(f"elapsed<0.5={elapsed < 0.5}")  # => Output: elapsed<0.5=True
    assert sorted(labels) == ["task-a", "task-b", "task-c"]  # => co-24: all three tasks actually completed and returned
    assert elapsed < 0.5  # => co-24: THREE tasks x 0.2s each ran in well under 0.6s -- proof they overlapped, not serialized
    # => co-24: if these ran SEQUENTIALLY (one session, one await at a time), elapsed would be >= 0.6s; running in
    # => under 0.5s is the measured evidence that asyncio.gather() truly interleaved the three sessions' I/O waits
    await engine.dispose()  # => closes every pooled async connection -- good hygiene at process shutdown
    print("ex-63 OK")  # => Output: ex-63 OK


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    asyncio.run(main())  # => starts the event loop and runs `main()` to completion -- the standard async entry point
