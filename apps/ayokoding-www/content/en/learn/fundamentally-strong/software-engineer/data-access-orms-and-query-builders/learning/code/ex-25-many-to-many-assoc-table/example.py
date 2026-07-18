# pyright: strict
"""Example 25: Many-to-Many -- a Plain Association Table."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Column, Engine, ForeignKey, Integer, Table, create_engine, text  # => co-09: Table builds a link table
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


student_course = Table(  # => co-09: a plain Core Table, NOT a mapped class -- it carries no extra columns of its own
    "student_course",  # => the link table's physical name -- convention: both parent names, singular, joined
    Base.metadata,  # => registers this Table alongside the mapped classes below, so create_all() builds it too
    Column[int]("student_id", Integer, ForeignKey("student.id"), primary_key=True),  # => half of the composite PK
    Column[int]("course_id", Integer, ForeignKey("course.id"), primary_key=True),  # => the other half -- one row per pairing
    # => Column[int] pins the generic explicitly -- Table/Column's own constructor overloads can't fully infer it alone
)  # => co-09: the composite primary key prevents the SAME student/course pair from being linked twice


class Student(Base):  # => co-09: one side of the many-to-many
    __tablename__ = "student"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    courses: Mapped[list["Course"]] = relationship(secondary=student_course, back_populates="students")  # => co-09: secondary=
    # => tells relationship() to route THROUGH student_course rather than through a direct FK on Student itself


class Course(Base):  # => co-09: the other side of the many-to-many
    __tablename__ = "course"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    title: Mapped[str]  # => a required TEXT column
    students: Mapped[list[Student]] = relationship(secondary=student_course, back_populates="courses")  # => the reverse side


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build all three tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for student, course, AND student_course


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty student, course, and student_course tables

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Student(name="Ada")  # => a student who will take TWO courses
        algebra = Course(title="Algebra")  # => the first course
        physics = Course(title="Physics")  # => the second course
        ada.courses.append(algebra)  # => co-09: append() to a collection -- relationship() writes the link row for us
        ada.courses.append(physics)  # => a second link row, same student
        session.add(ada)  # => cascades: adding the student registers both courses AND both link rows
        session.commit()  # => flushes student, both course rows, then both student_course link rows, in dependency order

    with engine.begin() as conn:  # => a raw connection -- confirms the physical link table actually holds two rows
        link_count = conn.execute(text("SELECT COUNT(*) FROM student_course")).scalar_one()  # => bypasses the ORM entirely
    print(f"link_count={link_count}")  # => Output: link_count=2
    assert link_count == 2  # => co-09: one physical row per (student, course) pairing -- the association table IS the M:N
    # => contrast this with Examples 22-24's one-to-many: there, the FK lived directly on the "many" side's own table;
    # => here, NEITHER Student nor Course carries the other's id -- a third table holds the relationship itself
    print("ex-25 OK")  # => Output: ex-25 OK
