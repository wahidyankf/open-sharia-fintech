# pyright: strict
"""Example 26: Many-to-Many -- Navigating Both Sides of the Same Link."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Column, Engine, ForeignKey, Integer, Table, create_engine, text  # => co-09: Table builds a link table
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


student_course = Table(  # => co-09: the same plain association table shape as Example 25
    "student_course",  # => the link table's physical name
    Base.metadata,  # => registers this Table alongside the mapped classes below
    Column[int]("student_id", Integer, ForeignKey("student.id"), primary_key=True),  # => half of the composite PK
    Column[int]("course_id", Integer, ForeignKey("course.id"), primary_key=True),  # => the other half of the composite PK
)  # => this example's FOCUS is navigation, not construction -- the shape is intentionally the same as Example 25


class Student(Base):  # => co-09: one side of the many-to-many
    __tablename__ = "student"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    courses: Mapped[list["Course"]] = relationship(secondary=student_course, back_populates="students")  # => forward nav


class Course(Base):  # => co-09: the other side of the many-to-many
    __tablename__ = "course"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    title: Mapped[str]  # => a required TEXT column
    students: Mapped[list[Student]] = relationship(secondary=student_course, back_populates="courses")  # => reverse nav


def reset_schema(engine: Engine) -> None:  # => shared reset helper -- wipes the whole schema, self-contained
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build all three tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for student, course, AND student_course


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    reset_schema(engine)  # => fresh, empty student, course, and student_course tables

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Student(name="Ada")  # => one student
        # => this example wires up a SHARED course on purpose -- it is what makes the reverse navigation below interesting
        grace = Student(name="Grace")  # => a second student, sharing one of Ada's courses
        algebra = Course(title="Algebra")  # => a course BOTH students take
        physics = Course(title="Physics")  # => a course only Ada takes -- proves the forward list below isn't hardcoded
        ada.courses.extend([algebra, physics])  # => co-09: extend() on the collection -- two link rows for Ada
        grace.courses.append(algebra)  # => co-09: Grace shares Algebra with Ada -- a THIRD link row, same course_id
        # => THREE distinct student_course rows total: (ada, algebra), (ada, physics), (grace, algebra)
        session.add_all([ada, grace])  # => cascades: both students, both courses, and all three link rows in one call
        session.commit()  # => flushes everything, in dependency order
        ada_id, algebra_id = ada.id, algebra.id  # => read INSIDE the session -- avoids DetachedInstanceError below

    with Session(engine) as session:  # => a FRESH session -- reloads from Postgres to prove BOTH directions persisted
        reloaded_ada = session.get(Student, ada_id)  # => session.get(): a single-PK lookup
        assert reloaded_ada is not None  # => the row exists
        forward = sorted(course.title for course in reloaded_ada.courses)  # => co-09: Student -> courses, forward direction
        print(f"ada's courses: {forward}")  # => Output: ada's courses: ['Algebra', 'Physics']

        reloaded_algebra = session.get(Course, algebra_id)  # => same lookup, from the OTHER side
        assert reloaded_algebra is not None  # => the row exists
        backward = sorted(student.name for student in reloaded_algebra.students)  # => co-09: Course -> students, REVERSE
        # => co-09: `.students` navigates AWAY from Course, back toward Student -- through the exact same student_course rows
        print(f"algebra's students: {backward}")  # => Output: algebra's students: ['Ada', 'Grace']

    assert forward == ["Algebra", "Physics"] and backward == ["Ada", "Grace"]  # => co-09: ONE link table, TWO navigable
    # => directions -- `.courses` and `.students` are both real Python collections, backed by the same physical rows
    print("ex-26 OK")  # => Output: ex-26 OK
