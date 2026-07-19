"""capstone-solid-core: typed request/response models (topic 11 HTTP JSON API + topic 17 co-07
allow-list validation), reused unchanged from the Pass-1 capstone plus one addition for this
capstone's own new endpoint: `RecentCheckinPublic` (Step 3's EXPLAIN-guided-index endpoint).
`app/digest.py`'s own `HabitDigest` dataclass serves Step 3's concurrency story instead -- it is
never exposed over HTTP (see digest.py's own docstring for why), so it has no Pydantic response
model here. Every field FastAPI/Pydantic validates BEFORE any handler code runs -- a hostile or
malformed body never reaches the service/repository layers.
"""

from datetime import date

from pydantic import BaseModel, Field

# --- auth surface -- co-07 allow-list validation (topic 17) -------------------------------


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    # => an allow-list: only letters/digits/underscore -- rejects `admin'--` outright,
    # => before any handler code runs (topic 17 co-07)
    password: str = Field(
        min_length=8, max_length=128
    )  # => bounds only -- the HASH is what protects it


class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)


class UserPublic(BaseModel):
    id: int
    username: str
    created_at: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- habits + check-ins -- topic 11 CRUD + topic 10 normalized data -----------------------


class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class HabitPublic(BaseModel):
    id: int
    name: str
    created_at: str
    archived: bool
    checkin_count: int
    current_streak: (
        int  # => computed by app/domain.py's Habit.current_streak(), never stored
    )


class CheckinCreate(BaseModel):
    checkin_date: date | None = (
        None  # => omit to check in for TODAY; pass an explicit date to backfill
    )


class CheckinPublic(BaseModel):
    habit_id: int
    checkin_date: date
    checkin_count: int
    current_streak: int


# --- capstone-solid-core addition: recent check-ins (Step 3's SQL tuning) -----------------


class RecentCheckinPublic(BaseModel):
    checkin_date: date
