# pyright: strict
"""Example 61: Async + selectinload -- Eager Loading Avoids the Async Lazy-Load Pitfall."""

from __future__ import annotations

import asyncio  # => the event loop this async example's whole body runs under
import os  # => reads connection settings from the environment

from sqlalchemy import ForeignKey, select, text  # => co-24: select() is identical in sync and async
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine  # => co-24: the async counterparts of Engine/Session
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload  # => co-14: selectinload() itself is NOT async-specific

SQLA_URL: str = os.environ.get(  # => the SAME `+psycopg` URL string works for both sync and async engines
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-08: the "one" side of a one-to-many relationship
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list[Order]] = relationship(back_populates="customer")  # => co-08: navigable collection, LAZY by default


class Order(Base):  # => co-08: the "many" side, each row points back at exactly one Customer
    __tablename__ = "order_table"  # => named to avoid colliding with the SQL reserved word ORDER
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => co-08: the FK column backing the relationship
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse navigation, customer.orders <-> order.customer


async def reset_schema(engine: AsyncEngine) -> None:  # => an async reset helper -- `async with`, not `with`
    async with engine.begin() as conn:  # => `async with` -- awaits the connection AND the commit/rollback on exit
        await conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        await conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer/Order into
        await conn.run_sync(Base.metadata.create_all)  # => run_sync() bridges Core's sync DDL onto the async connection


async def main() -> None:  # => co-24: the async entry point -- everything below runs on the event loop asyncio.run() starts
    engine = create_async_engine(SQLA_URL)  # => an async-capable engine -- its pool hands out async connections
    await reset_schema(engine)  # => awaited -- schema setup happens before any query below runs

    async with AsyncSession(engine) as session:  # => the async counterpart of Session -- same API, `await`-ed calls
        ada = Customer(name="Ada", orders=[Order(), Order()])  # => co-24: builds the whole graph in memory before any I/O
        session.add(ada)  # => add() itself is NOT async -- it's pure in-memory bookkeeping
        await session.commit()  # => co-24: commit() IS async -- it issues the INSERTs over the network

    async with AsyncSession(engine) as session:  # => a FRESH async session -- the relationship starts fully unloaded
        stmt = select(Customer).options(selectinload(Customer.orders))  # => co-14: selectinload issues a SECOND query up front
        result = await session.execute(stmt)  # => co-24: ONE awaited round trip triggers BOTH the customer AND the eager order query
        loaded = result.scalars().one()  # => co-24: .scalars().one() itself is SYNC -- it just unpacks an already-fetched result
        order_count = len(loaded.orders)  # => co-14: NO further await needed -- .orders is already populated, not a lazy stub
        # => co-24 + co-14: this is the pitfall selectinload avoids -- touching an UNLOADED relationship attribute under
        # => async raises MissingGreenlet (Example 62), because a lazy SELECT can't run implicitly outside a greenlet;
        # => selectinload front-loads the data INSIDE the awaited execute() call, so no lazy trigger ever fires later

    print(f"order_count={order_count}")  # => Output: order_count=2
    assert order_count == 2  # => co-14: both orders arrived via the eager query, never via an implicit lazy SELECT
    await engine.dispose()  # => closes every pooled async connection -- good hygiene at process shutdown
    print("ex-61 OK")  # => Output: ex-61 OK


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    asyncio.run(main())  # => starts the event loop and runs `main()` to completion -- the standard async entry point
