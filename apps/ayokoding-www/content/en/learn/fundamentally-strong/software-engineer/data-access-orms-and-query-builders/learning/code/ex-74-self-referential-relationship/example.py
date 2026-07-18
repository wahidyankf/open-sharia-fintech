# pyright: strict
"""Example 74: An Adjacency-List Self-FK Tree -- Parent/Child Navigation on ONE Table."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import ForeignKey, create_engine, select, text  # => co-08: ForeignKey points the FK column BACK at its own table
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship  # => relationship() twice, one class

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Category(Base):  # => co-08: ONE table, but TWO relationship directions -- parent and children, both self-referential
    __tablename__ = "category"  # => the physical table name -- a single table models the whole tree
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"))  # => co-08: an FK pointing BACK at its own table
    children: Mapped[list[Category]] = relationship(back_populates="parent")  # => co-08: the "one" side -- a parent's list of direct children
    parent: Mapped[Category | None] = relationship(  # => co-08: the "many" side -- remote_side marks the PARENT's `id` column
        back_populates="children",
        remote_side=[id],  # => tells SQLAlchemy which end of the self-FK is the "one" in this pair
    )


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build Category's table into
    Base.metadata.create_all(engine)  # => issues CREATE TABLE category, including the self-referential FK constraint

    with Session(engine) as session:  # => a Session is the ORM's unit-of-work handle (co-12)
        electronics = Category(name="Electronics")  # => the ROOT of this small tree -- no parent
        laptops = Category(name="Laptops", parent=electronics)  # => co-08: `parent=` assigns the self-FK via the OBJECT, not an id
        phones = Category(name="Phones", parent=electronics)  # => a SECOND child, same parent, same pattern
        session.add(electronics)  # => cascades: adding the root also registers laptops and phones via the relationship
        session.commit()  # => flushes all three rows -- Electronics FIRST, then Laptops/Phones (co-12's dependency ordering)

    with Session(engine) as session:  # => a FRESH session -- nothing cached, navigation reloads from the database
        root = session.execute(select(Category).where(Category.name == "Electronics")).scalars().one()  # => loads the root row
        child_names = sorted(c.name for c in root.children)  # => co-08: navigates DOWN the tree via `.children`
        laptop = session.execute(select(Category).where(Category.name == "Laptops")).scalars().one()  # => loads a leaf row
        parent_name = laptop.parent.name if laptop.parent is not None else None  # => co-08: navigates UP the tree via `.parent`

    # => co-08: `laptop.parent` above triggered its OWN lazy SELECT -- a self-referential relationship is still just
    # => a relationship, subject to the SAME lazy/eager choices (co-13, co-14) as any other foreign-key mapping
    print(f"child_names={child_names}")  # => Output: child_names=['Laptops', 'Phones']
    print(f"parent_name={parent_name}")  # => Output: parent_name=Electronics
    assert child_names == ["Laptops", "Phones"]  # => co-08: downward navigation returns BOTH children, correctly ordered
    assert parent_name == "Electronics"  # => co-08: upward navigation returns the SAME root the children were built from
    # => co-08: ONE table (`category`), ONE self-pointing foreign key (`parent_id`), and TWO relationship() directions
    # => model an entire tree -- no separate parent table, no separate child table; this is the standard
    # => adjacency-list pattern for hierarchies (org charts, comment threads, category trees) in a relational schema
    print("ex-74 OK")  # => Output: ex-74 OK
