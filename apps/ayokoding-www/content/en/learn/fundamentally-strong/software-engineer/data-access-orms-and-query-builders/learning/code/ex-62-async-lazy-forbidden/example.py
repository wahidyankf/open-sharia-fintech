# pyright: strict
"""Example 62: Lazy Access Under Async Raises -- You Must Eager-Load or Await Explicitly."""

from __future__ import annotations

import asyncio  # => the event loop this async example's whole body runs under
import os  # => reads connection settings from the environment

from sqlalchemy import ForeignKey, select, text  # => co-24: select() is identical in sync and async
from sqlalchemy.exc import MissingGreenlet  # => co-24 + co-16: the specific exception an implicit lazy load raises under async
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, AsyncSession, create_async_engine  # => co-16: AsyncAttrs is the escape hatch
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SAME `+psycopg` URL string works for both sync and async engines
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(AsyncAttrs, DeclarativeBase):  # => co-16: mixing in AsyncAttrs adds an `.awaitable_attrs` escape hatch to every mapped class
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-08: the "one" side of a one-to-many relationship
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    orders: Mapped[list[Order]] = relationship(back_populates="customer")  # => co-13: LAZY by default -- no eager options here


class Order(Base):  # => co-08: the "many" side, each row points back at exactly one Customer
    __tablename__ = "order_table"  # => named to avoid colliding with the SQL reserved word ORDER
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))  # => co-08: the FK column backing the relationship
    customer: Mapped[Customer] = relationship(back_populates="orders")  # => the reverse navigation, deliberately LEFT lazy


async def reset_schema(engine: AsyncEngine) -> None:  # => an async reset helper -- `async with`, not `with`
    async with engine.begin() as conn:  # => `async with` -- awaits the connection AND the commit/rollback on exit
        await conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        await conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer/Order into
        await conn.run_sync(Base.metadata.create_all)  # => run_sync() bridges Core's sync DDL onto the async connection


async def main() -> None:  # => co-24: the async entry point -- everything below runs on the event loop asyncio.run() starts
    engine = create_async_engine(SQLA_URL)  # => an async-capable engine -- its pool hands out async connections
    await reset_schema(engine)  # => awaited -- schema setup happens before any query below runs

    async with AsyncSession(engine) as session:  # => the async counterpart of Session -- same API, `await`-ed calls
        session.add(Customer(name="Ada", orders=[Order()]))  # => builds the whole graph in memory before any I/O
        await session.commit()  # => commit() IS async -- it issues the INSERTs over the network

    async with AsyncSession(engine) as session:  # => a FRESH async session -- .orders starts fully unloaded on purpose
        order = (await session.execute(select(Order))).scalars().one()  # => co-24: loads the Order row itself, not its relationship

        raised = False  # => tracks whether the forbidden lazy access actually raised, rather than silently succeeding
        try:  # => co-16: touching `.customer` outside an eager-loaded/awaited path is the mistake this example reproduces
            _ = order.customer.name  # => co-13: this is PLAIN attribute access -- SQLAlchemy tries an implicit lazy SELECT
        except MissingGreenlet:  # => co-24: the async driver has no synchronous fallback to run that implicit SELECT on
            raised = True  # => confirms the guard fired instead of silently blocking or returning stale data

        awaited_customer = await order.awaitable_attrs.customer  # => co-16: AsyncAttrs' escape hatch -- an EXPLICIT awaited lazy load
        # => co-16: `.awaitable_attrs.customer` performs the SAME lazy SELECT as plain `.customer`, but as a coroutine
        # => you explicitly `await` -- it turns an accidental blocking call into an intentional, visible one, exactly
        # => the way raiseload() (co-16, sync) turns a silent lazy query into a loud error instead of a hidden cost

    # => co-24 + co-16: sync SQLAlchemy would have silently run the extra SELECT here -- async refuses to guess, forcing
    # => the choice between an eager-loading strategy (Example 61) or an explicit awaited access, right here
    print(f"raised={raised}")  # => Output: raised=True
    print(f"awaited_customer_name={awaited_customer.name}")  # => Output: awaited_customer_name=Ada
    assert raised  # => co-24: plain lazy attribute access is genuinely forbidden under async, not just discouraged
    assert awaited_customer.name == "Ada"  # => co-16: the SAME data is reachable -- just through an explicit awaited path
    await engine.dispose()  # => closes every pooled async connection -- good hygiene at process shutdown
    print("ex-62 OK")  # => Output: ex-62 OK


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    asyncio.run(main())  # => starts the event loop and runs `main()` to completion -- the standard async entry point
