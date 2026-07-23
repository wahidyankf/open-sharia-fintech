"""Example 12: Run via uvicorn."""

from fastapi import FastAPI  # => the web framework this whole tier builds on

app = FastAPI()  # => uvicorn imports THIS exact module-level name ("app:app")


@app.get("/")  # => decorator-based ROUTING: GET "/" maps to read_root
def read_root() -> dict[str, str]:
    """A minimal route so the dev loop (co-22) has something to hit."""
    return {"served_by": "uvicorn"}  # => confirms which process answered


# => no "if __name__" block needed: uvicorn IMPORTS this module and reads the
# => module-level `app` object directly -- "app:app" means "module app, attr app"
# => contrast this with Examples 1-9, which each need serve_forever() to
# => run standalone -- uvicorn is the thing that plays that role here instead
