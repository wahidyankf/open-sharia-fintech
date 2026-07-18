# pyright: strict
"""Capstone Step 3: relationships_and_n_plus_1.py -- object graph, identity map, unit of work, N+1.

Assumes seed.py already ran. Walks relationships, the identity map, N+1, and a transaction rollback
against the SHARED seeded data (read-only), then a throwaway "Scratch Team" walks session states, the
unit of work, and both cascade-delete mechanisms (co-22) -- restoring the dataset to seed.py's exact
original counts so migration_and_bulk.py (Step 4) can assume that same baseline.
"""

from __future__ import annotations  # => enables modern type-hint syntax across this file

import os  # => reads connection settings from the environment
from collections.abc import Generator  # => the modern return-type annotation @contextmanager expects, not Iterator
from contextlib import contextmanager  # => co-15: a reusable "count queries in this block" helper, same shape as Example 42
from decimal import Decimal  # => money-shaped totals are Decimal, never float -- exact, no rounding drift
from typing import Any  # => types SQLAlchemy's own untyped event-hook callback arguments

from sqlalchemy import Engine, ForeignKey, create_engine, event, inspect, select  # => co-11: inspect() reads InstanceState
from sqlalchemy.exc import InvalidRequestError  # => co-16: the exact exception a raiseload()-guarded access raises
from sqlalchemy.orm import (  # => co-06: every ORM name this file needs, imported from one place
    DeclarativeBase,  # => co-06: the shared mapper registry root every mapped class below inherits from
    InstanceState,  # => co-11: the live per-object state inspect() returns
    Mapped,  # => co-06: the typed-attribute wrapper every mapped column and relationship uses
    Session,  # => co-11 + co-12: the unit-of-work handle every function below opens at least once
    mapped_column,  # => co-06: declares a column backing a Mapped[] attribute
    raiseload,  # => co-16: the loud-failure guard
    relationship,  # => co-08: declares a navigable link between two mapped classes
    selectinload,  # => co-14: the eager-loading fix for co-15's N+1
)

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example",  # => the fallback default
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Team(Base):  # => co-06: maps onto the table seed.py already created -- mapping is decoupled from creation
    __tablename__ = "team"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    members: Mapped[list["Member"]] = relationship(  # => co-08: the one-to-many side
        back_populates="team",  # => keeps Team.members and Member.team in sync in memory
        cascade="all, delete-orphan",  # => co-22: the ORM's OWN cascade -- deleting a Team also deletes its Members,
        # => even though the plain team_id FK below carries no "ON DELETE CASCADE" at the database level at all
    )  # => end of Team.members' relationship() call


class Member(Base):  # => co-06 + co-08: the "many" side of team --< member
    __tablename__ = "member"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))  # => the FK column every JOIN below walks
    team: Mapped[Team] = relationship(back_populates="members")  # => the reverse, many-to-one navigation
    assignments: Mapped[list["Assignment"]] = relationship(  # => co-13: default lazy loading
        back_populates="member",  # => keeps Member.assignments and Assignment.member in sync in memory
        passive_deletes=True,  # => co-22: tells the ORM NOT to null out assignment.member_id before a delete -- the
        # => database's own "ON DELETE CASCADE" (seed.py's schema) removes those rows instead, so the ORM should
        # => step out of the way rather than trying to manage a column that is part of assignment's composite PK
    )  # => end of Member.assignments' relationship() call


class Task(Base):  # => co-06: the other side of the member <-> task many-to-many link
    __tablename__ = "task"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    title: Mapped[str]  # => a required TEXT column
    status: Mapped[str]  # => 'open' or 'done' -- Step 4's bulk update targets this column
    assignments: Mapped[list["Assignment"]] = relationship(  # => co-09: navigates VIA the association object
        back_populates="task",  # => keeps Task.assignments and Assignment.task in sync in memory
        passive_deletes=True,  # => co-22: same reasoning as Member.assignments above -- let the DATABASE's own
        # => "ON DELETE CASCADE" clean up assignment rows when a Task is deleted (Step 3g exercises this directly)
    )  # => end of Task.assignments' relationship() call


class Assignment(Base):  # => co-09: the ASSOCIATION OBJECT -- a real mapped class, not a bare link table
    __tablename__ = "assignment"  # => the physical M:N link table seed.py created, modeled as a full class
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), primary_key=True)  # => half of the composite PK
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), primary_key=True)  # => the other half of the composite PK
    hours_logged: Mapped[Decimal]  # => co-09: the EXTRA column a plain two-column link table has no natural place for
    member: Mapped[Member] = relationship(back_populates="assignments")  # => navigates back to the Member side
    task: Mapped[Task] = relationship(back_populates="assignments")  # => navigates back to the Task side


@contextmanager  # => co-15: turns "count every SELECT fired inside this block" into a plain `with` statement
def query_counter(engine: Engine) -> Generator[list[int]]:  # => yields a one-element mutable box holding the running count
    box = [0]  # => a list, not a plain int -- the caller reads box[0] AFTER the block exits, still seeing live updates

    def on_execute(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:  # => untyped hook params (SQLAlchemy's own)
        if statement.strip().upper().startswith("SELECT"):  # => this counter only cares about read traffic
            box[0] += 1  # => increments the SAME box the caller holds a reference to

    listener = event.listens_for(engine, "before_cursor_execute")(on_execute)  # => attaches for the block's duration
    try:  # => the caller's code runs HERE, between attach and detach
        yield box  # => hands the box to the `with` block -- readable both during and after
    finally:  # => detaches even if the caller's block raises
        event.remove(engine, "before_cursor_execute", listener)  # => cleanup -- the NEXT measurement starts at zero


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, reused across every step below

    # --- Step 3a: the identity map (co-10) -- read-only, against the shared seeded data ---
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12), and owns ONE identity map
        by_query = session.execute(select(Member).where(Member.name == "Ada")).scalar_one()  # => query #1: fetches Ada
        by_get = session.get(Member, by_query.id)  # => co-10: same primary key, same session -- served from the IDENTITY
        # => MAP, no second SELECT at all, and it is the exact SAME Python object, not merely an equal one
        print(f"identity_map_same_object={by_query is by_get}")  # => Output: identity_map_same_object=True
        assert by_query is by_get  # => co-10: `is`, not `==` -- one Python object per primary key within this session

    # --- Step 3b: reproduce the N+1 (co-13, co-15) -- default lazy loading, read-only ---
    with query_counter(engine) as before:  # => co-15: measures the UNFIXED, lazy-default access pattern
        with Session(engine) as session:  # => a FRESH session -- nothing cached
            members = session.execute(select(Member)).scalars().all()  # => query #1: all 5 members, Barbara included
            for member in members:  # => this loop is the N+1 itself -- ONE lazy SELECT per member, even Barbara's empty one
                _ = [a.hours_logged for a in member.assignments]  # => co-13: each access fires its OWN round trip
    print(f"n_plus_1_before={before[0]} queries")  # => Output: n_plus_1_before=6 queries
    assert before[0] == 6  # => co-15: 1 parent query + 5 members, INCLUDING Barbara's -- lazy loading fires regardless
    # => of whether the relationship turns out empty; the round trip itself is the cost, not the row count it returns

    # --- Step 3c: the eager-loading fix (co-14) -- same access pattern, read-only ---
    with query_counter(engine) as after:  # => co-14: the SAME access pattern, now eager-loaded up front
        with Session(engine) as session:  # => a FRESH session -- nothing cached
            stmt = select(Member).options(selectinload(Member.assignments))  # => co-14: batches ALL 5 members' children
            members = session.execute(stmt).scalars().all()  # => query #1 (parents) + query #2 (batched children)
            for member in members:  # => identical loop to Step 3b -- but `.assignments` is already loaded in memory
                _ = [a.hours_logged for a in member.assignments]  # => reads from memory, contributes zero new SELECTs
    print(f"n_plus_1_after={after[0]} queries")  # => Output: n_plus_1_after=2 queries
    assert after[0] == 2  # => co-15: the fix collapses N+1 down to a CONSTANT 2, regardless of how many members exist

    # --- Step 3d: the raiseload guard (co-16) -- read-only, catches the exact failure Step 3b just reproduced ---
    with Session(engine) as session:  # => a FRESH session -- the guard below applies to THIS query only
        stmt = select(Member).options(raiseload(Member.assignments))  # => co-16: forbids `.assignments` from lazy-loading
        guarded = session.execute(stmt).scalars().all()  # => fetches ONLY the 5 member rows -- exactly like the default
        try:  # => the access below is EXACTLY what Step 3b's loop did on purpose, forbidden here on purpose
            _ = guarded[0].assignments  # => co-16: touching a raiseload()-guarded relationship never silently queries
            raise AssertionError("expected InvalidRequestError")  # => fails loudly if SQLAlchemy's behavior ever changes
        except InvalidRequestError as exc:  # => co-16: a LOUD, immediate error instead of a silent extra round trip
            print(f"raiseload_guard_raised={type(exc).__name__}")  # => Output: raiseload_guard_raised=InvalidRequestError

    # --- Step 3e: an ORM transaction rollback (co-17) -- mutates, then reverts, the shared seeded data ---
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = session.execute(select(Member).where(Member.name == "Ada")).scalar_one()  # => loads the SAME Ada as Step 3a
        ada.name = "Ada (uncommitted rename)"  # => co-12: the unit of work marks `ada` DIRTY -- no SQL sent yet
        session.rollback()  # => co-17: discards the uncommitted UPDATE AND expires every object this session tracked
        print(f"after_rollback_name={ada.name}")  # => Output: after_rollback_name=Ada -- expiry forces a fresh SELECT
        assert ada.name == "Ada"  # => co-17: the rename never reached the database -- rollback restored the ORIGINAL row

    # --- Step 3f: session states (co-11) + unit of work dirty tracking (co-12), on a THROWAWAY scratch team ---
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        scratch_team = Team(name="Scratch Team", members=[Member(name="Scratch A"), Member(name="Scratch B")])
        state: InstanceState[Team] = inspect(scratch_team)  # => a handle onto the object's own InstanceState (co-11)
        print(f"transient={state.transient}")  # => Output: transient=True -- STATE 1: constructed, no Session has added it
        assert state.transient  # => co-11: exactly one phase flag is ever True at a time

        session.add(scratch_team)  # => co-11: STATE 2 -- PENDING. cascades: the 2 scratch members are pending too
        print(f"pending={state.pending}")  # => Output: pending=True
        assert state.pending and not state.transient  # => moved out of transient the instant the session saw it

        session.flush()  # => co-12: the unit of work issues the INSERTs now -- team FIRST, members SECOND (FK order)
        print(f"new_before_commit={len(session.new)} objects still new")  # => Output: new_before_commit=0 objects still new
        assert len(session.new) == 0  # => co-12: flush() cleared the "new" set -- every pending object now has a real PK
        scratch_a = scratch_team.members[0]  # => reads the flushed Member back through the relationship, PK now assigned
        scratch_a.name = "Scratch A (renamed)"  # => co-12: marks scratch_a DIRTY -- the unit of work tracks this too
        print(f"dirty_before_commit={scratch_a in session.dirty}")  # => Output: dirty_before_commit=True
        assert scratch_a in session.dirty  # => co-12: session.dirty is exactly the set flush() will UPDATE next

        session.commit()  # => co-11 + co-12: STATE 3 -- PERSISTENT. flushes the pending rename, then commits everything
        print(f"persistent={state.persistent}")  # => Output: persistent=True
        assert state.persistent and not state.pending  # => co-11: the object graph is now fully durable
        scratch_team_id = scratch_team.id  # => reads `id` INSIDE the still-open session -- avoids a DetachedInstanceError

    print(f"detached={state.detached}")  # => Output: detached=True
    assert state.detached  # => co-11: STATE 4 -- the `with` block closed the session; scratch_team still exists in
    # => Python memory, still has its `id`, but is no longer tracked by ANY session's identity map or unit of work

    # --- Step 3g: two cascade DELETE flavors (co-22), cleaning the scratch team fully back out ---
    with Session(engine) as session:  # => co-09: attaches ONE scratch assignment, linking the scratch team's own member
        scratch_team_reloaded = session.get(Team, scratch_team_id)  # => reloads the persistent-but-detached scratch team
        assert scratch_team_reloaded is not None  # => narrows Optional for pyright --strict
        scratch_member = scratch_team_reloaded.members[0]  # => co-08: navigates the relationship to grab a real Member
        scratch_task = Task(title="Scratch Task", status="open")  # => co-06: a throwaway task, deleted later this step
        session.add(Assignment(member=scratch_member, task=scratch_task, hours_logged=Decimal("1.00")))  # => co-09
        session.commit()  # => flushes the scratch task AND the scratch assignment linking it to the scratch member
        scratch_task_id = scratch_task.id  # => reads `id` INSIDE the still-open session

    with Session(engine) as session:  # => co-22 flavor 1: the DATABASE's own "ON DELETE CASCADE" (seed.py's schema)
        scratch_task_reloaded = session.get(Task, scratch_task_id)  # => reloads the scratch task by its real PK
        assert scratch_task_reloaded is not None  # => narrows Optional for pyright --strict
        session.delete(scratch_task_reloaded)  # => the ORM issues a plain DELETE FROM task WHERE id = ... -- no ORM
        # => cascade config on Task.assignments at all; the scratch assignment row still vanishes, because seed.py's
        # => own "task_id INT ... REFERENCES task(id) ON DELETE CASCADE" is a DATABASE constraint, not an ORM one --
        # => it fires for ANY delete that reaches the database, regardless of which tier (raw SQL, builder, or ORM) issued it
        session.commit()  # => the scratch task, AND its scratch assignment row, are both gone after this single commit

    with Session(engine) as session:  # => co-22 flavor 2: the ORM's OWN "cascade=all, delete-orphan" (Team.members above)
        scratch_team_reloaded = session.get(Team, scratch_team_id)  # => reloads the scratch team one final time
        assert scratch_team_reloaded is not None  # => narrows Optional for pyright --strict
        session.delete(scratch_team_reloaded)  # => co-22: the ORM sees cascade="all, delete-orphan" on Team.members and
        # => issues DELETE FROM member WHERE team_id = ... BEFORE DELETE FROM team -- entirely in Python-side relationship
        # => config, since team_id itself carries NO "ON DELETE CASCADE" at the database level (contrast seed.py's plain FK)
        session.commit()  # => both scratch members AND the scratch team are now gone

        remaining_teams = session.execute(select(Team)).scalars().all()  # => a final count, back to seed.py's baseline
        remaining_members = session.execute(select(Member)).scalars().all()  # => co-22: confirms the cascade left no orphans
        remaining_tasks = session.execute(select(Task)).scalars().all()  # => confirms Step 3g's own scratch task is gone
        remaining_assignments = session.execute(select(Assignment)).scalars().all()  # => confirms the scratch link is gone
    counts = (len(remaining_teams), len(remaining_members), len(remaining_tasks), len(remaining_assignments))
    print(f"final_counts_teams_members_tasks_assignments={counts}")  # => Output: final_counts_teams_members_tasks_assignments=(2, 5, 5, 6)
    assert counts == (2, 5, 5, 6)  # => co-22: BOTH cascade-delete flavors cleaned up completely -- exactly seed.py's baseline
    print("relationships_and_n_plus_1.py OK")  # => Output: relationships_and_n_plus_1.py OK
