# pyright: strict
"""Capstone Step 1: seed.py -- schema + seed data over the raw PEP 249 DB-API (co-02, co-05).

Unlike every ex-NN example (each resets and seeds its OWN tables), this capstone's four scripts
share ONE persistent schema: seed.py runs first, the other three build on what it leaves behind.
"""

from __future__ import annotations

import os  # => reads connection settings from the environment (co-01)

import psycopg  # => co-02: the raw PEP 249 DB-API -- no builder, no ORM involved in seeding
# => this file never imports SQLAlchemy, PyPika, or peewee -- pure raw DB-API only, co-01's floor tier

PG_DSN: str = os.environ.get("PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example")  # => a plain DB-API DSN
# => override PG_DSN in the environment to point every capstone script at a different Postgres instance
# => a DB-API DSN, distinct from the SQLAlchemy-dialect URL the other three capstone scripts each build


def seed() -> None:
    # => reset + load, in ONE function -- every other capstone script assumes this exact starting state
    # => called once by __main__ below, and importable directly by anything that wants a fresh dataset
    with psycopg.connect(PG_DSN, autocommit=True) as conn:  # => autocommit: DDL needs no explicit commit
        # => the DROP+CREATE pair below is the entire "reset" half of this function's contract
        conn.execute("DROP SCHEMA public CASCADE")  # => wipes EVERY table -- a clean slate for the whole capstone
        conn.execute("CREATE SCHEMA public")  # => a blank public schema, shared by all four capstone scripts
        # => everything from here down is the "load" half -- four CREATE TABLEs, then four INSERTs

        # => team --< member: a plain FK, NO "ON DELETE CASCADE" at the database level -- deleting a team
        # => with members still attached fails at the DATABASE unless the caller removes them first, OR the
        # => ORM's own cascade="all, delete-orphan" relationship option does it for you (co-22, Step 3).
        # => four tables total: team (1), member (many), task (many), assignment (the M2M link, co-09)
        conn.execute("CREATE TABLE team(id SERIAL PRIMARY KEY, name TEXT NOT NULL)")  # => the "one" side of team-member
        conn.execute(
            "CREATE TABLE member(id SERIAL PRIMARY KEY, name TEXT NOT NULL, team_id INT NOT NULL REFERENCES team(id))"  # => NO ON DELETE CASCADE here
        )
        conn.execute("CREATE TABLE task(id SERIAL PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL)")  # => no FK of its own
        # => member >--< task via assignment: co-09's association OBJECT shape -- a composite primary key
        # => PLUS an extra hours_logged column a plain two-column link table has no natural place for. This
        # => FK pair DOES carry "ON DELETE CASCADE" -- the opposite contrast to team/member's plain FK above:
        # => deleting a member or a task cleans up its assignment rows at the DATABASE level, no ORM cascade
        # => configuration required at all (co-22, Step 3 contrasts both flavors side by side).
        conn.execute(
            "CREATE TABLE assignment(member_id INT NOT NULL REFERENCES member(id) ON DELETE CASCADE, task_id INT NOT NULL REFERENCES task(id) ON DELETE CASCADE, hours_logged NUMERIC(6,2) NOT NULL, PRIMARY KEY (member_id, task_id))"  # => co-09: composite PK (member_id, task_id) IS the association object's own identity
        )

        # => 2 teams -- Platform (3 members) and Growth (2 members), an intentionally uneven split
        conn.execute("INSERT INTO team(name) VALUES (%s), (%s)", ("Platform", "Growth"))  # => team.id 1=Platform, 2=Growth
        # => 5 members: Barbara (id 5) deliberately gets ZERO assignments below -- exercises the LEFT JOIN /
        # => outer-join edge case every tier's report (Step 2) and the N+1 measurement (Step 3) must both handle
        conn.execute(
            "INSERT INTO member(name, team_id) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)",  # => 5 (name, team_id) pairs -- member.id auto-assigned 1-5
            (
                "Ada",  # => member.id 1
                1,  # => team_id 1 = Platform
                "Grace",  # => member.id 2
                1,  # => team_id 1 = Platform
                "Linus",  # => member.id 3
                2,  # => team_id 2 = Growth
                "Margaret",  # => member.id 4
                2,  # => team_id 2 = Growth
                "Barbara",  # => member.id 5 -- the ZERO-assignment member (co-15 edge case)
                1,  # => team_id 1 = Platform
            ),
        )
        # => 5 tasks: "Plan Q3 roadmap" (id 5) deliberately gets ZERO assignments -- the task-side mirror
        # => of Barbara's zero-assignment member row, exercising the SAME edge case from the other direction
        conn.execute(
            "INSERT INTO task(title, status) VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)",  # => 5 (title, status) pairs -- task.id auto-assigned 1-5
            (
                "Set up CI pipeline",  # => task.id 1
                "done",  # => already completed before this capstone even starts
                "Design onboarding flow",  # => task.id 2
                "open",  # => still in progress
                "Write API docs",  # => task.id 3
                "open",  # => still in progress
                "Fix login bug",  # => task.id 4
                "done",  # => already completed
                "Plan Q3 roadmap",  # => task.id 5 -- gets ZERO assignments below (co-15 edge case, task side)
                "open",  # => the outer-join edge case this task exists to exercise
            ),
        )
        # => 6 assignment rows linking 4 of the 5 members to 4 of the 5 tasks, each carrying its own
        # => hours_logged (co-09's extra column) -- Ada and Linus each touch 2 tasks, Grace and Margaret 1 each
        conn.execute(
            "INSERT INTO assignment(member_id, task_id, hours_logged) VALUES "  # => 6 (member_id, task_id, hours_logged) triples
            "(%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)",  # => 18 placeholders total, 3 per row
            (
                1,  # => member_id 1 = Ada
                1,  # => task_id 1 = "Set up CI pipeline"
                8.5,  # => Ada on "Set up CI pipeline"
                1,  # => member_id 1 = Ada again -- a SECOND assignment for this member
                4,  # => task_id 4 = "Fix login bug"
                3.0,  # => Ada on "Fix login bug"
                2,  # => member_id 2 = Grace
                2,  # => task_id 2 = "Design onboarding flow"
                5.0,  # => Grace on "Design onboarding flow"
                3,  # => member_id 3 = Linus
                3,  # => task_id 3 = "Write API docs"
                4.5,  # => Linus on "Write API docs"
                3,  # => member_id 3 = Linus again -- a SECOND assignment for this member
                4,  # => task_id 4 = "Fix login bug"
                2.0,  # => Linus on "Fix login bug"
                4,  # => member_id 4 = Margaret
                2,  # => task_id 2 = "Design onboarding flow"
                6.0,  # => Margaret on "Design onboarding flow"
            ),
        )


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    seed()  # => builds the schema and loads the dataset every later capstone script reads
    # => a fresh connection here, separate from the one seed() used, just to print a verification count
    with psycopg.connect(PG_DSN) as conn:  # => a fresh connection, just to print a verification count
        # => one query, four scalar subqueries -- co-02: plain PEP 249 DB-API, no builder or ORM needed
        counts = conn.execute(
            "SELECT (SELECT count(*) FROM team), (SELECT count(*) FROM member), (SELECT count(*) FROM task), (SELECT count(*) FROM assignment)"  # => 4 counts in one round trip
        ).fetchone()
    assert counts is not None  # => narrows Optional for pyright --strict -- the query above always returns exactly 1 row
    teams, members, tasks, assignments = counts  # => unpacks the 4-column verification row
    print(f"teams={teams} members={members} tasks={tasks} assignments={assignments}")  # => Output: teams=2 members=5 tasks=5 assignments=6
    assert (teams, members, tasks, assignments) == (2, 5, 5, 6)  # => co-02: confirms every row landed exactly as seeded
    # => (2, 5, 5, 6) is the fixed baseline every other capstone script (Steps 2-4) assumes is present
    print("seed.py OK")  # => Output: seed.py OK
