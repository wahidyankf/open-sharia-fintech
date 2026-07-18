# pyright: strict
"""Capstone Step 2: report_three_tiers.py -- "total hours per team," answered 3 ways (co-01).

Assumes seed.py already ran. Computed once per tier of Example 1's spectrum, then asserted to agree.
"""

from __future__ import annotations  # => enables modern type-hint syntax across this file

import os  # => reads connection settings from the environment
from decimal import Decimal  # => money-shaped totals are Decimal, never float -- exact, no rounding drift
from typing import LiteralString, cast  # => acknowledges a runtime-built string is safe to execute (see tier2)

import psycopg  # => co-02: tier 1 -- the raw PEP 249 DB-API, also how tier 2's PyPika-built SQL actually runs
from pypika import Query, Table  # => co-03: tier 2 -- PyPika composes the query as data, not concatenated text
from pypika import functions as fn  # => co-04: PyPika's own Sum/Coalesce aggregate functions
from sqlalchemy import ForeignKey, create_engine, func, select  # => co-01: tier 3 -- SQLAlchemy's own select() + func namespace
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship  # => co-06: typed declarative mapping

PG_DSN: str = os.environ.get("PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example")  # => plain DB-API DSN
SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example",  # => the fallback default
)  # => override SQLA_URL in the environment to point at a different Postgres instance


def tier1_raw_sql() -> list[tuple[str, Decimal]]:  # => co-01: tier 1 of 3 -- the raw-SQL floor
    # => hand-written SQL over the PEP 249 DB-API (co-02) -- every join and column typed by hand
    with psycopg.connect(PG_DSN) as conn:  # => a fresh connection -- no builder, no ORM in between
        rows = conn.execute(  # => a plain string-literal double-JOIN, COALESCE for teams/members with zero hours
            "SELECT t.name, COALESCE(SUM(a.hours_logged), 0) FROM team t JOIN member m ON m.team_id = t.id LEFT JOIN assignment a ON a.member_id = m.id GROUP BY t.id, t.name ORDER BY t.name"  # => COALESCE handles zero-hour teams
        ).fetchall()  # => co-01: this list of raw tuples is what tiers 2 and 3 below must reproduce exactly
    return [(str(r[0]), Decimal(r[1])) for r in rows]  # => casts each column so all 3 tiers compare equal


def tier2_query_builder() -> list[tuple[str, Decimal]]:  # => co-01: tier 2 of 3 -- the query-builder middle
    # => the SAME report, composed as data via PyPika (co-03, co-04) -- no string concatenation
    team_t, member_t, assignment_t = Table("team"), Table("member"), Table("assignment")  # => 3 Table VALUES, not strings
    query = (  # => the builder tree is built up one method call at a time, below
        Query.from_(team_t)  # => start the builder tree from team
        .join(member_t)  # => .join() (INNER) takes another Table value -- every team has at least 1 member here
        .on(member_t.team_id == team_t.id)  # => .on() takes a PyPika expression object, not raw text
        .left_join(assignment_t)  # => .left_join(): a member with zero assignments still contributes a row
        .on(assignment_t.member_id == member_t.id)  # => the outer-join condition, also composed, not interpolated
        .groupby(team_t.id, team_t.name)  # => GROUP BY composed onto the SAME tree, one method at a time
        .orderby(team_t.name)  # => matches tier 1's ORDER BY, so the two result lists compare equal
        .select(team_t.name, fn.Coalesce(fn.Sum(assignment_t.hours_logged), 0))  # => co-04: PyPika's own aggregate functions
    )  # => the tree only becomes SQL text when you ask for it -- nothing has run yet
    with psycopg.connect(PG_DSN) as conn:  # => co-01: PyPika BUILT the query, but a plain DB-API cursor still RUNS it
        sql_text = cast(LiteralString, str(query))  # => str(query) renders the tree; cast() vouches it is safe to run
        rows = conn.execute(sql_text).fetchall()  # => the DB-API executes PyPika's OUTPUT exactly like tier 1's own SQL
    return [(str(r[0]), Decimal(r[1])) for r in rows]  # => identical shape to tier 1's return value


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase (tier 3)
    pass  # => carries no columns -- purely a registry root


class Team(Base):  # => co-06: maps onto the table seed.py already created -- mapping is decoupled from creation
    __tablename__ = "team"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    members: Mapped[list["Member"]] = relationship(back_populates="team")  # => co-08: the one-to-many side


class Member(Base):  # => co-06 + co-08: the "many" side of team --< member
    __tablename__ = "member"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))  # => co-08: the FK column the JOIN below walks
    team: Mapped[Team] = relationship(back_populates="members")  # => the reverse, many-to-one navigation


class ReportAssignment(Base):  # => co-06 + co-09: maps onto the SAME assignment table seed.py created
    __tablename__ = "assignment"  # => the physical association-object table (co-09) seed.py created
    member_id: Mapped[int] = mapped_column(primary_key=True)  # => half of the composite PK
    task_id: Mapped[int] = mapped_column(primary_key=True)  # => the other half of the composite PK
    hours_logged: Mapped[Decimal]  # => the extra column this report sums, identical to tiers 1 and 2


def tier3_orm() -> list[tuple[str, Decimal]]:  # => co-01: tier 3 of 3 -- the full ORM, aggregation still server-side
    # => the SAME report through SQLAlchemy's select() (co-06) -- entities in, rows out
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        stmt = (  # => the SAME shape as tier 1/2: JOIN, LEFT JOIN, GROUP BY, ORDER BY -- expressed via mapped entities
            select(Team.name, func.coalesce(func.sum(ReportAssignment.hours_logged), 0))  # => co-01: aggregate columns
            .select_from(Team)  # => anchors the query on the mapped Team entity, not a bare table name
            .join(Member, Member.team_id == Team.id)  # => co-08: the mapped relationship's own join condition, reused
            .outerjoin(ReportAssignment, ReportAssignment.member_id == Member.id)  # => co-01: LEFT JOIN, same as tiers 1 and 2
            .group_by(Team.id, Team.name)  # => matches tier 1/2's GROUP BY exactly
            .order_by(Team.name)  # => matches tier 1/2's ORDER BY, so all 3 result lists compare equal
        )
        rows = session.execute(stmt).all()  # => co-25: aggregation computed server-side, identical to tiers 1 and 2
    return [(str(r[0]), Decimal(r[1])) for r in rows]  # => identical shape to tiers 1 and 2's return values


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    sql_result = tier1_raw_sql()  # => co-01: tier 1 -- raw SQL
    builder_result = tier2_query_builder()  # => co-01: tier 2 -- query builder
    orm_result = tier3_orm()  # => co-01: tier 3 -- full ORM
    print(f"sql_result={sql_result}")  # => Output: sql_result=[('Growth', Decimal('12.50')), ('Platform', Decimal('16.50'))]
    print(f"builder_result={builder_result}")  # => Output: identical to sql_result
    print(f"orm_result={orm_result}")  # => Output: identical to sql_result
    assert sql_result == builder_result == orm_result  # => co-01 + co-25 + co-26: all three tiers agree on ONE correct answer
    # => co-25 + co-26: raw SQL (tier 1) and the query builder (tier 2) express this GROUP BY report about as
    # => directly as the ORM (tier 3) does here -- a REPORT like this is exactly the shape where a query
    # => builder or raw SQL usually stays the simpler choice in practice (co-27), while the ORM tier earns its
    # => keep on CRUD and object-graph navigation instead (Step 3 below exercises exactly that side of the tradeoff)
    print("report_three_tiers.py OK")  # => Output: report_three_tiers.py OK
