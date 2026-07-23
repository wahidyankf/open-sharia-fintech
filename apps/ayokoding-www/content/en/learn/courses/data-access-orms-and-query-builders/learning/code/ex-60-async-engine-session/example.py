# pyright: strict
"""Example 60: create_async_engine + AsyncSession -- an Async Query Round-Trips."""

from __future__ import annotations

import asyncio  # => co-24: the event loop this async example's whole body runs under
import os  # => reads connection settings from the environment

from sqlalchemy import select, text  # => co-24: select() works identically in sync and async -- only EXECUTION is different
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine  # => co-24: the async counterparts of Engine/Session
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

SQLA_URL: str = os.environ.get(  # => co-24: the SAME `+psycopg` URL string works for BOTH sync and async engines
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => the async engine constructor, not the URL, is what selects async mode -- override SQLA_URL to repoint it


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-24: the SAME kind of mapped class as every sync example -- mapping itself is NOT async-specific
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


async def reset_schema(engine: AsyncEngine) -> None:  # => co-24: an async reset helper -- `async with`, not `with`
    async with engine.begin() as conn:  # => co-24: `async with` -- awaits the connection AND the commit/rollback on exit
        await conn.execute(text("DROP SCHEMA public CASCADE"))  # => co-24: every DB call is now `await`-ed, never blocking
        await conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
        await conn.run_sync(Base.metadata.create_all)  # => co-24: run_sync() bridges Core's sync DDL onto the async connection


async def main() -> None:  # => co-24: the async entry point -- everything below runs on the event loop asyncio.run() starts
    engine = create_async_engine(SQLA_URL)  # => co-24: an async-capable engine -- its pool hands out async connections
    await reset_schema(engine)  # => co-24: awaited -- schema setup happens before any query below runs

    async with AsyncSession(engine) as session:  # => co-24: the async counterpart of Session -- same API, `await`-ed calls
        session.add(Customer(name="Ada"))  # => co-24: add() itself is NOT async -- it's pure in-memory bookkeeping
        await session.commit()  # => co-24: commit() IS async -- it issues the actual INSERT over the network

    async with AsyncSession(engine) as session:  # => a FRESH async session, just to read back the row
        result = await session.execute(select(Customer))  # => co-24: execute() is async -- awaits the round trip to Postgres
        customers = result.scalars().all()  # => co-24: .scalars().all() itself is SYNC -- it just unpacks an already-fetched result

    names = [c.name for c in customers]  # => reads the loaded objects' names
    # => co-24: this whole `main()` never once blocks the event loop on network I/O -- every DB round trip yields control
    print(f"names={names}")  # => Output: names=['Ada']
    assert names == ["Ada"]  # => co-24: the async round trip inserted AND read back the same row correctly

    await engine.dispose()  # => co-24: closes every pooled async connection -- good hygiene at process shutdown
    # => co-24: the ORM's OWN mapping (DeclarativeBase, Mapped[]) is identical between sync and async -- what changes is
    # => the ENGINE, the SESSION class, and that every DATABASE-touching call must now be awaited; Example 62 shows
    # => the one operation that does NOT get an async-safe equivalent by default: touching an unloaded relationship
    print("ex-60 OK")  # => Output: ex-60 OK


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    asyncio.run(main())  # => co-24: starts the event loop and runs `main()` to completion -- the standard async entry point
