"""capstone-solid-core: the re-engineered Habit Tracker API -- the imperative shell (topic
21 SOLID + topic 22/23 functional core / imperative shell split) that wires the pure functional
core (domain.py), the port + adapter (ports.py / repository_sqlite.py), and the application
layer (services.py) into a running FastAPI app. Route handlers below are deliberately thin:
parse the request, call ONE `HabitService` method, shape the response -- no business rule lives
here (Single Responsibility, topic 21). Auth (auth.py) and the two middlewares (middleware.py)
are reused BYTE-IDENTICAL from the Pass-1 capstone -- proven correct there, unchanged here.

Run with: uvicorn app.main:app --port 8101
"""

import os
import sqlite3
from collections.abc import Iterator
from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import auth
from . import repository_sqlite as repo
from .domain import Habit
from .middleware import make_token_check_middleware, security_headers_middleware
from .models import (
    CheckinCreate,
    CheckinPublic,
    HabitCreate,
    HabitPublic,
    RecentCheckinPublic,
    TokenResponse,
    UserLogin,
    UserPublic,
    UserRegister,
)
from .services import HabitService

# overridable so tests can point at a fresh, isolated file
DB_PATH = os.environ.get(
    "CAPSTONE_SOLID_CORE_DB_PATH", os.path.join(os.path.dirname(__file__), "habits.db")
)
# REQUIRED, no hardcoded fallback -- refuses to start if the secret is missing, by design
AUTH_SECRET = os.environ["CAPSTONE_SOLID_CORE_AUTH_SECRET"]

repo.init_db(
    DB_PATH
)  # => applies schema_v1 + migration_v2 + migration_v3 once, at startup

app = FastAPI(title="capstone-solid-core: Habit Tracker API (Pass-2 professional core)")


def get_db() -> Iterator[sqlite3.Connection]:  # => one connection per request
    conn = repo.get_connection(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def get_habit_service(
    conn: sqlite3.Connection = Depends(get_db),
) -> HabitService:
    """Composition root (topic 21 DIP): the ONE place a concrete `SqliteHabitRepository` is
    constructed and handed to `HabitService` as its abstract `HabitRepository` port. Every
    route handler below depends on `HabitService`, never on `repo`/`sqlite3` directly."""
    return HabitService(repo.SqliteHabitRepository(conn))


def _resolve_token(token: str) -> int | None:  # => the ONE place AUTH_SECRET is used
    return auth.resolve_token(token, AUTH_SECRET)


def _current_user_id(request: Request) -> int:
    user_id = getattr(
        request.state, "user_id", None
    )  # => set by the token-check middleware
    assert user_id is not None  # => guaranteed once token_check_middleware has run
    return int(user_id)


app.middleware("http")(make_token_check_middleware(_resolve_token))  # guards /habits
app.middleware("http")(security_headers_middleware)  # stamps every response


@app.exception_handler(
    StarletteHTTPException
)  # => registered on Starlette's BASE class
async def handle_http_exception(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    # => fastapi.HTTPException is a SUBCLASS of Starlette's, so this one handler also catches
    # => exceptions Starlette raises internally (unmatched-route 404s, wrong-method 405s)
    body = (
        exc.detail
        if isinstance(exc.detail, dict)
        else {"error": {"code": "error", "message": str(exc.detail)}}
    )
    return JSONResponse(status_code=exc.status_code, content=body)


def _habit_to_public(conn: sqlite3.Connection, habit: Habit) -> HabitPublic:
    """One shared place that turns a domain `Habit` into the HTTP response shape."""
    row = conn.execute(
        "SELECT created_at FROM habits WHERE id = ?", (habit.id,)
    ).fetchone()
    assert row is not None  # => the caller only ever passes a habit it just loaded
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
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail={"error": {"code": "conflict", "message": "username already taken"}},
        )
    password_hash = auth.hash_password(
        body.password
    )  # => hash BEFORE it ever touches the DB
    return repo.create_user(conn, body.username, password_hash)


@app.post("/auth/login", response_model=TokenResponse)
def login_route(
    body: UserLogin, conn: sqlite3.Connection = Depends(get_db)
) -> TokenResponse:
    row = repo.get_user_by_username(conn, body.username)
    generic_error = (
        HTTPException(  # => SAME message for "no such user" and "wrong password"
            status_code=401,
            detail={
                "error": {
                    "code": "unauthorized",
                    "message": "invalid username or password",
                }
            },
        )
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
    body: HabitCreate,
    request: Request,
    conn: sqlite3.Connection = Depends(get_db),
    service: HabitService = Depends(get_habit_service),
) -> HabitPublic:
    user_id = _current_user_id(request)
    habit = service.create_habit(user_id, body)
    return _habit_to_public(conn, habit)


# guarded -- token required (reads are user-scoped)
@app.get("/habits", response_model=list[HabitPublic])
def list_habits_route(
    request: Request,
    q: str | None = Query(default=None, max_length=200),
    include_archived: bool = Query(default=False),
    conn: sqlite3.Connection = Depends(get_db),
    service: HabitService = Depends(get_habit_service),
) -> list[HabitPublic]:
    user_id = _current_user_id(request)
    habits = service.list_habits(user_id, include_archived, q)
    return [_habit_to_public(conn, h) for h in habits]


# guarded -- token required, ownership-scoped
@app.get("/habits/{habit_id}", response_model=HabitPublic)
def get_habit_route(
    habit_id: int,
    request: Request,
    conn: sqlite3.Connection = Depends(get_db),
    service: HabitService = Depends(get_habit_service),
) -> HabitPublic:
    user_id = _current_user_id(request)
    habit = service.get_habit(habit_id, user_id)
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
    service: HabitService = Depends(get_habit_service),
) -> CheckinPublic:
    user_id = _current_user_id(request)
    checkin_day = body.checkin_date if body.checkin_date is not None else date.today()
    habit = service.record_checkin(habit_id, user_id, checkin_day)
    if habit is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such habit"}},
        )
    return CheckinPublic(
        habit_id=habit_id,
        checkin_date=checkin_day,
        checkin_count=habit.checkin_count(),
        current_streak=habit.current_streak(date.today()),
    )


@app.post("/habits/{habit_id}/archive", response_model=HabitPublic)
def archive_habit_route(
    habit_id: int,
    request: Request,
    conn: sqlite3.Connection = Depends(get_db),
    service: HabitService = Depends(get_habit_service),
) -> HabitPublic:
    user_id = _current_user_id(request)
    habit = service.archive_habit(habit_id, user_id)
    if habit is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such habit"}},
        )
    return _habit_to_public(conn, habit)


# guarded -- token required, ownership-scoped
@app.delete("/habits/{habit_id}", status_code=204)
def delete_habit_route(
    habit_id: int,
    request: Request,
    service: HabitService = Depends(get_habit_service),
) -> None:
    user_id = _current_user_id(request)
    if not service.delete_habit(habit_id, user_id):
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "no such habit"}},
        )


# Step 3's EXPLAIN-guided-index endpoint (topic 26) -- no join, no sort at the DB level; see
# migration_v3.sql + bench/explain_query_plan.sh for the real, captured before/after plan.
@app.get("/habits/activity/recent", response_model=list[RecentCheckinPublic])
def recent_activity_route(
    request: Request,
    limit: int = Query(default=20, ge=1, le=200),
    service: HabitService = Depends(get_habit_service),
) -> list[RecentCheckinPublic]:
    user_id = _current_user_id(request)
    rows = service.recent_activity(user_id, limit)
    return [RecentCheckinPublic(checkin_date=date.fromisoformat(d)) for _, d in rows]
