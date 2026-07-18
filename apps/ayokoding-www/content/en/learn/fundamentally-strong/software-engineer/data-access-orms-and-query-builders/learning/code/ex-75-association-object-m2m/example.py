# pyright: strict
"""Example 75: An Association OBJECT -- Extra Columns on a Many-to-Many Link, Not Just Two Foreign Keys."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import ForeignKey, create_engine, select, text  # => co-09: ForeignKey twice -- one per side of the M:N pair
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship  # => relationship() links the association object both ways

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Student(Base):  # => co-09: one side of the M:N pair -- reached only THROUGH Enrollment, not a bare table
    __tablename__ = "student"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    enrollments: Mapped[list[Enrollment]] = relationship(back_populates="student")  # => co-09: navigates VIA the association object


class Course(Base):  # => co-09: the other side of the M:N pair -- same pattern as Student
    __tablename__ = "course"  # => the physical table name
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    title: Mapped[str]  # => a required TEXT column
    enrollments: Mapped[list[Enrollment]] = relationship(back_populates="course")  # => co-09: navigates VIA the association object


class Enrollment(Base):  # => co-09: the ASSOCIATION OBJECT -- a real mapped class, not a bare link table like Example 25
    __tablename__ = "enrollment"  # => the physical M:N link table, but modeled as a full class
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)  # => half of the composite PK
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)  # => the other half of the composite PK
    grade: Mapped[str]  # => co-09: the EXTRA column a plain association table (Example 25) has no natural place for
    student: Mapped[Student] = relationship(back_populates="enrollments")  # => navigates back to the Student side
    course: Mapped[Course] = relationship(back_populates="enrollments")  # => navigates back to the Course side


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build all three tables into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE for student, course, and the enrollment association object

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        ada = Student(name="Ada")  # => the student half of the link this example creates
        calculus = Course(title="Calculus")  # => the course half of the link
        enrollment = Enrollment(student=ada, course=calculus, grade="A")  # => co-09: the EXTRA `grade` column, set right here
        session.add(enrollment)  # => cascades: adding the enrollment also registers ada and calculus
        session.commit()  # => flushes all three rows -- student, course, and the enrollment link WITH its grade

    with Session(engine) as session:  # => a FRESH session -- nothing cached, navigation reloads from the database
        loaded = session.execute(select(Enrollment)).scalars().one()  # => co-09: loads the association object ITSELF, not just a link row
        student_name = loaded.student.name  # => co-09: navigates FROM the association object TO the Student
        course_title = loaded.course.title  # => co-09: navigates FROM the association object TO the Course
        grade = loaded.grade  # => co-09: the EXTRA attribute -- persisted and reloaded, exactly like any other mapped column

    print(f"student_name={student_name}")  # => Output: student_name=Ada
    print(f"course_title={course_title}")  # => Output: course_title=Calculus
    print(f"grade={grade}")  # => Output: grade=A
    assert (student_name, course_title, grade) == ("Ada", "Calculus", "A")  # => co-09: all three round-tripped correctly
    # => co-09: a plain association TABLE (Example 25) has no natural place for a per-link attribute like a grade,
    # => an enrollment date, or a role -- an association OBJECT is a full mapped class sitting on that same link
    # => table, so it can carry arbitrary extra columns AND be queried, updated, and navigated like any other entity
    print("ex-75 OK")  # => Output: ex-75 OK
