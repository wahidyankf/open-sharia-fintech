# pyright: strict
"""Example 21: Active Record (peewee) vs Data Mapper (SQLAlchemy) -- the Same Write."""

from __future__ import annotations

import os  # => reads connection settings from the environment

import peewee  # => co-07: the Active Record library
from sqlalchemy import create_engine, text  # => co-07: the Data Mapper library
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

PG_HOST: str = os.environ.get("PG_HOST", "localhost")  # => override for CI / non-default hosts
PG_PORT: int = int(os.environ.get("PG_PORT", "5432"))  # => Postgres' conventional default port
PG_DB: str = os.environ.get("PG_DB", "orm_by_example")  # => one shared database, every example resets its own tables
PG_USER: str = os.environ.get("PG_USER", "postgres")  # => local trust-auth Postgres convention
PG_PASSWORD: str = os.environ.get("PG_PASSWORD", "postgres")  # => matches PG_USER for local dev
SQLA_URL: str = f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"  # => the ORM's own URL form


def write_active_record() -> int:  # => co-07: Active Record -- returns the id peewee assigned
    db = peewee.PostgresqlDatabase(PG_DB, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    # => a fresh peewee database handle, scoped inside this function -- keeps the two tiers fully independent

    class BaseModel(peewee.Model):  # => a fresh Model registry, scoped inside this function
        class Meta:  # => peewee's own configuration mechanism -- a nested Meta class, not a constructor argument
            database = db  # => every subclass of BaseModel persists through `db`

    class Customer(BaseModel):  # => co-07: THE OBJECT persists itself -- no separate mapper/session object exists
        id = peewee.AutoField()  # => explicit primary key -- peewee auto-adds this at runtime even if omitted
        name = peewee.CharField()

    db.connect()  # => co-07: peewee's OWN connection -- there is no separate "session" concept
    db.drop_tables([Customer], safe=True, cascade=True)  # pyright: ignore[reportUnknownMemberType]  # => idempotent reset
    db.create_tables([Customer])  # pyright: ignore[reportUnknownMemberType]  # => issues CREATE TABLE

    ada = Customer(name="Ada")  # => build the object
    ada.save()  # pyright: ignore[reportUnknownMemberType]  # => THE OBJECT calls .save() on ITSELF -- Active Record's defining trait
    db.close()  # => peewee has no context-manager Session -- closing is a manual, separate step
    return ada.id  # => the assigned primary key


class Base(DeclarativeBase):  # => co-06 + co-07: Data Mapper -- the mapped class itself carries no persistence behavior
    pass  # => carries no columns -- purely a registry root


class DmCustomer(Base):  # => co-07: renamed to avoid colliding with peewee's own Customer class above
    __tablename__ = "customer"  # => the physical table name -- same shape as the Active Record example, different class
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


def write_data_mapper() -> int:  # => co-07: Data Mapper -- returns the id the ORM assigned
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, entirely separate from the mapped DmCustomer class
    # => the engine, not DmCustomer, owns the connection -- the mapped class stays a plain data-holding object
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema, shared with the peewee run above
    Base.metadata.create_all(engine)  # => issues CREATE TABLE customer from DmCustomer's Mapped[] fields

    with Session(engine) as session:  # => co-07: a SEPARATE Session object does the persisting -- the mapper's job
        ada = DmCustomer(name="Ada")  # => build the object -- DmCustomer itself has NO .save() method at all
        session.add(ada)  # => the SESSION registers the object, not the object registering itself
        session.commit()  # => the SESSION flushes and commits -- DmCustomer never talks to Postgres directly
        return ada.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    ar_id = write_active_record()  # => runs the peewee (Active Record) path
    dm_id = write_data_mapper()  # => runs the SQLAlchemy (Data Mapper) path
    # => both paths write the SAME logical row ("Ada") to the SAME physical customer table, one tier at a time
    print(f"active_record id={ar_id}, data_mapper id={dm_id}")  # => Output: active_record id=1, data_mapper id=1
    assert ar_id == 1 and dm_id == 1  # => both tiers persisted their FIRST row as id=1 -- same outcome, different API shape
    # => co-07: peewee's object called .save() on ITSELF; SQLAlchemy's SESSION called .add()/.commit() on the object
    # => Fowler's PoEAA names this exact split: Active Record couples persistence to the object; Data Mapper separates them
    print("ex-21 OK")  # => Output: ex-21 OK
