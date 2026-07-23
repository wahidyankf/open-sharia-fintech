"""Pass-1 capstone: Habit Tracker -- the hardened HTTP JSON API tying every Pass-1 topic
together: routing + validation (11), a normalized SQLite DB (10), an OO domain model (08)
built on an apt hash-set (07), argon2id auth + injection-safety + headers + env secrets (17).

Run with: uvicorn app.main:app --port 8100  (this doc's canonical prose port; the actual
verification runs captured on this page may use other ports to avoid colliding with other
locally running servers -- see each transcript for the exact port it used).
"""

import os
import sqlite3
from collections.abc import Iterator
from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import auth
from . import repository as repo
from .domain import Habit
from .middleware import make_token_check_middleware, security_headers_middleware
from .models import (
    CheckinCreate,
    CheckinPublic,
    HabitCreate,
    HabitPublic,
    TokenResponse,
    UserLogin,
    UserPublic,
    UserRegister,
)

# overridable so tests can point at a fresh, isolated file
DB_PATH = os.environ.get(
    "CAPSTONE1_DB_PATH", os.path.join(os.path.dirname(__file__), "habits.db")
)
# REQUIRED, no hardcoded fallback -- this line raises KeyError and refuses to
# start if the secret is missing, by design (topic 17)
AUTH_SECRET = os.environ["CAPSTONE1_AUTH_SECRET"]

repo.init_db(DB_PATH)  # => applies schema_v1.sql + migration_v2.sql once, at startup

app = FastAPI(title="Pass-1 Capstone: Habit Tracker API")


def get_db() -> Iterator[sqlite3.Connection]:  # => one connection per request
    conn = repo.get_connection(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def _resolve_token(token: str) -> int | None:  # => the ONE place AUTH_SECRET is used
    return auth.resolve_token(token, AUTH_SECRET)


def _current_user_id(request: Request) -> int:
    # => set by the token-check middleware below
    user_id = getattr(request.state, "user_id", None)
    # => guaranteed once token_check_middleware has run for this path
    assert user_id is not None
    return int(user_id)


app.middleware("http")(make_token_check_middleware(_resolve_token))  # guards /habits
app.middleware("http")(security_headers_middleware)  # stamps every response


# => registered on Starlette's BASE HTTPException
@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    # => fastapi.HTTPException (raised by every route below) is a SUBCLASS of Starlette's, so this
    # => one handler also catches exceptions Starlette itself raises internally -- unmatched-route 404s,
    # => wrong-method 405s -- giving the SAME {"error": {...}} envelope app-wide, not just route-raised ones.
    body = (
        exc.detail
        if isinstance(exc.detail, dict)
        else {"error": {"code": "error", "message": str(exc.detail)}}
    )
    return JSONResponse(status_code=exc.status_code, content=body)


def _habit_to_public(conn: sqlite3.Connection, habit: Habit) -> HabitPublic:
    """One shared place that turns a domain `Habit` into the HTTP response shape -- every route
    below calls this instead of repeating the same five-field mapping (and the streak-as-of-today
    computation) four separate times."""
    row = conn.execute(
        "SELECT created_at FROM habits WHERE id = ?", (habit.id,)
    ).fetchone()
    # => the caller only ever passes a habit it just loaded/created/updated
    assert row is not None
    return HabitPublic(
        id=habit.id,
        name=habit.name,
        created_at=str(row["created_at"]),
        archived=habit.archived,
        checkin_count=habit.checkin_count(),
        current_streak=habit.current_streak(date.today()),
    )


@app.get("/health")  # => LIVENESS -- always 200, no DB dependency at all
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")  # => READINESS -- genuinely pings the database
def ready(
    response: Response, conn: sqlite3.Connection = Depends(get_db)
) -> dict[str, str]:
    try:
        repo.ping(conn)
        return {"status": "ready"}
    except sqlite3.OperationalError as exc:
        response.status_code = 503
        return {"status": "not_ready", "reason": str(exc)}


@app.post("/auth/register", response_model=UserPublic, status_code=201)
def register_route(
    body: UserRegister, conn: sqlite3.Connection = Depends(get_db)
) -> UserPublic:
    existing = repo.get_user_by_username(conn, body.username)
    # => a specific, honest conflict -- distinct from login's generic error
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail={"error": {"code": "conflict", "message": "username already taken"}},
        )
    # => hash BEFORE it ever touches the DB
    password_hash = auth.hash_password(body.password)
    return repo.create_user(conn, body.username, password_hash)


@app.post("/auth/login", response_model=TokenResponse)
def login_route(
    body: UserLogin, conn: sqlite3.Connection = Depends(get_db)
) -> TokenResponse:
    row = repo.get_user_by_username(conn, body.username)
    # => SAME message for "no such user" and "wrong password" -- an attacker
    # => probing usernames learns nothing from the response either way
    generic_error = HTTPException(
        status_code=401,
        detail={
            "error": {"code": "unauthorized", "message": "invalid username or password"}
        },
    )
    if row is None:
        raise generic_error
    if not auth.verify_password(str(row["password_hash"]), body.password):
        raise generic_error
    token = auth.issue_token(int(row["id"]), AUTH_SECRET)
    return TokenResponse(access_token=token)


# guarded: token required
@app.post("/habits", response_model=HabitPublic, status_code=201)
def create_habit_route(
    body: HabitCreate, request: Request, conn: sqlite3.Connection = Depends(get_db)
) -> HabitPublic:
    user_id = _current_user_id(request)
    habit = repo.create_habit(conn, user_id, body)
    return _habit_to_public(conn, habit)


# guarded -- token required (reads are user-scoped)
@app.get("/habits", response_model=list[HabitPublic])
def list_habits_route(
    request: Request,
    # => co-03 (topic 17): FIXED, parameterized search
    q: str | None = Query(default=None, max_length=200),
    include_archived: bool = Query(default=False),
    conn: sqlite3.Connection = Depends(get_db),
) -> list[HabitPublic]:
    user_id = _current_user_id(request)
    habits = (
        repo.search_habits(conn, user_id, q)
        if q
        else repo.list_habits(conn, user_id, include_archived)
    )
    return [_habit_to_public(conn, h) for h in habits]


# guarded -- token required, ownership-scoped
@app.get("/habits/{habit_id}", response_model=HabitPublic)
def get_habit_route(
    habit_id: int, request: Request, conn: sqlite3.Connection = Depends(get_db)
) -> HabitPublic:
    user_id = _current_user_id(request)
    habit = repo.get_habit(conn, habit_id, user_id)
    if habit is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such habit"}},
        )
    return _habit_to_public(conn, habit)


@app.post("/habits/{habit_id}/checkins", response_model=CheckinPublic, status_code=201)
def record_checkin_route(
    habit_id: int,
    body: CheckinCreate,
    request: Request,
    conn: sqlite3.Connection = Depends(get_db),
) -> CheckinPublic:
    user_id = _current_user_id(request)
    habit = repo.get_habit(conn, habit_id, user_id)
    if habit is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such habit"}},
        )
    checkin_day = body.checkin_date if body.checkin_date is not None else date.today()
    repo.record_checkin(conn, habit_id, checkin_day.isoformat())
    # => mirror the write into the in-memory domain object too, so the response
    # => below reflects it without a second DB round trip
    habit.record_checkin(checkin_day)
    return CheckinPublic(
        habit_id=habit_id,
        checkin_date=checkin_day,
        checkin_count=habit.checkin_count(),
        current_streak=habit.current_streak(date.today()),
    )


@app.post("/habits/{habit_id}/archive", response_model=HabitPublic)
def archive_habit_route(
    habit_id: int, request: Request, conn: sqlite3.Connection = Depends(get_db)
) -> HabitPublic:
    user_id = _current_user_id(request)
    habit = repo.archive_habit(conn, habit_id, user_id)
    if habit is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such habit"}},
        )
    return _habit_to_public(conn, habit)


# guarded -- token required, ownership-scoped
@app.delete("/habits/{habit_id}", status_code=204)
def delete_habit_route(
    habit_id: int, request: Request, conn: sqlite3.Connection = Depends(get_db)
) -> None:
    user_id = _current_user_id(request)
    if not repo.delete_habit(conn, habit_id, user_id):
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such habit"}},
        )
