# pyright: strict
"""Example 43: session.begin() -- Commit on Success, Rollback on Error."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Engine, create_engine, select, text  # => co-17: select() confirms what actually survived
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Customer(Base):  # => co-17: the table this example writes to, once successfully and once NOT
    __tablename__ = "customer"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column, UNIQUE below to force the second attempt to fail


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Customer's table into
        conn.execute(text("CREATE TABLE customer (id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL)"))  # => raw DDL, adds UNIQUE
    # => Base.metadata.create_all() is skipped here on purpose -- the UNIQUE constraint above needs raw DDL, since
    # => Customer's own Mapped[str] doesn't declare uniqueness, and this example wants a REAL constraint violation


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty customer table with a UNIQUE name constraint

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        with session.begin():  # => co-17: an EXPLICIT transaction scope -- commits automatically on a clean exit
            session.add(Customer(name="Ada"))  # => the FIRST, successful write
        # => co-17: `session.begin()`'s own `with` block already committed here -- no separate session.commit() needed

        try:  # => the block below deliberately violates the UNIQUE constraint on `name`
            with session.begin():  # => co-17: a SECOND transaction scope -- rolls back automatically on any exception
                session.add(Customer(name="Ada"))  # => the SAME name -- Postgres will reject this at flush/commit time
        except Exception as exc:  # => co-17: the UNIQUE violation propagates as a real exception, not a silent no-op
            print(f"raised: {type(exc).__name__}")  # => Output: raised: IntegrityError
            # => co-17: `session.begin()`'s `with` block caught the exception, rolled back, and RE-RAISED it here --
            # => the failed second Ada was never durably written, even though `session.add()` itself never complained

    with Session(engine) as session:  # => a FRESH session, just to read back the final state
        names = session.execute(select(Customer.name)).scalars().all()  # => co-17: confirms what actually persisted
        print(f"names={names}")  # => Output: names=['Ada']
        assert names == ["Ada"]  # => co-17: exactly ONE Ada survived -- the committed write, not the rolled-back one
    # => co-17: `with session.begin():` is the idiomatic pattern -- commit on success, rollback on ANY exception,
    # => with no manual try/except/commit/rollback bookkeeping required at the call site itself
    print("ex-43 OK")  # => Output: ex-43 OK
