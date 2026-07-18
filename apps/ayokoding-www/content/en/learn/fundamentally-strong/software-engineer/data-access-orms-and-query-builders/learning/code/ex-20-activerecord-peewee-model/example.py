# pyright: strict
"""Example 20: Active Record -- peewee Model.create()/.save()."""

from __future__ import annotations

import os  # => reads connection settings from the environment

import peewee  # => co-07: peewee is this topic's Active Record library

PG_HOST: str = os.environ.get("PG_HOST", "localhost")  # => override for CI / non-default hosts
PG_PORT: int = int(os.environ.get("PG_PORT", "5432"))  # => Postgres' conventional default port
PG_DB: str = os.environ.get("PG_DB", "orm_by_example")  # => one shared database, every example resets its own tables
PG_USER: str = os.environ.get("PG_USER", "postgres")  # => local trust-auth Postgres convention
PG_PASSWORD: str = os.environ.get("PG_PASSWORD", "postgres")  # => matches PG_USER for local dev
db = peewee.PostgresqlDatabase(PG_DB, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)  # => co-07's connection


class BaseModel(peewee.Model):  # => a shared base so every peewee Model in this file uses the SAME database
    class Meta:  # => peewee's own configuration mechanism -- a nested Meta class, not a constructor argument
        database = db  # => every subclass of BaseModel persists through `db`


class Customer(BaseModel):  # => co-07: the object itself knows how to save -- Active Record's defining trait
    id = peewee.AutoField()  # => explicit primary key -- peewee auto-adds this at RUNTIME even if you omit it
    name = peewee.CharField()  # => a required TEXT-like column, peewee's CharField


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    db.connect()  # => co-07: peewee manages its OWN connection, not a separate Session object
    db.drop_tables([Customer], safe=True, cascade=True)  # pyright: ignore[reportUnknownMemberType]  # => idempotent reset
    db.create_tables([Customer])  # pyright: ignore[reportUnknownMemberType]  # => issues CREATE TABLE from Customer's fields

    ada = Customer(name="Ada")  # => constructs an in-memory instance -- not yet a row in Postgres
    ada.save()  # pyright: ignore[reportUnknownMemberType]  # => co-07: THE OBJECT persists ITSELF -- no separate session.add()
    print(f"after save: id={ada.id}")  # => Output: after save: id=1
    # => contrast with Example 16 (SQLAlchemy): there, a SEPARATE Session object called session.add()/session.commit()

    grace = Customer.create(name="Grace")  # pyright: ignore[reportUnknownMemberType]  # => .create(): construct + save in one call
    print(f"after create: id={grace.id}")  # => Output: after create: id=2

    count = Customer.select().count()  # pyright: ignore[reportUnknownMemberType]  # => Customer itself exposes the query API too
    print(f"count={count}")  # => Output: count=2
    assert count == 2  # => both Ada (via .save()) and Grace (via .create()) persisted
    db.close()  # => releases the connection -- peewee has no context-manager Session to do this automatically
    # => co-07: peewee's dynamic Active-Record API is a genuine typing trade-off -- the `pyright: ignore` comments above
    # => document a REAL upstream gap in peewee's own stubs, contrasted with SQLAlchemy's fully static Mapped[] typing
    print("ex-20 OK")  # => Output: ex-20 OK
