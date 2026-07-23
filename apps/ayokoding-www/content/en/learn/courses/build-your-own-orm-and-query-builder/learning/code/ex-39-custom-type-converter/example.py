"""Example 39: Register a Custom Type Converter for a JSON Column."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import json  # => the JSON encode/decode pair backing this custom converter
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => a decoded JSON value can be any JSON-representable Python type


CONVERTERS: dict[str, Any] = {  # => co-12: a per-column-type CONVERTER REGISTRY, not hardcoded logic
    "json": (json.dumps, json.loads),  # => (on_store, on_load) pair -- one entry per custom type
}  # => adding a new custom type means adding ONE entry here, never touching the coerce_* functions


def coerce_on_store(column_type: str, value: Any) -> Any:  # => looks up the registered encoder
    encode, _ = CONVERTERS[column_type]  # => picks the store-side half of the registered pair
    return encode(value)  # => runs it -- a dict becomes a JSON text string here


def coerce_on_load(column_type: str, raw: Any) -> Any:  # => looks up the registered decoder
    _, decode = CONVERTERS[column_type]  # => picks the load-side half of the registered pair
    return decode(raw)  # => runs it -- a JSON text string becomes a dict again here


settings = {"theme": "dark", "notifications": True}  # => a Python dict the app wants to persist
stored_text = coerce_on_store("json", settings)  # => encoded THROUGH the registry, not ad hoc
assert stored_text == '{"theme": "dark", "notifications": true}'  # => real JSON text, byte-for-byte

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, settings TEXT)")  # => TEXT column, plain
    conn.execute("INSERT INTO users VALUES (1, ?)", (stored_text,))  # => co-02: parameterized insert
    conn.commit()  # => makes the stored JSON text visible
    raw = conn.execute("SELECT settings FROM users WHERE id = 1").fetchone()[0]  # => raw driver TEXT
    reloaded = coerce_on_load("json", raw)  # => decoded THROUGH the same registry, symmetric with store
    assert reloaded == settings  # => the round trip preserves every key and value
    print(reloaded)  # => Output: {'theme': 'dark', 'notifications': True}
