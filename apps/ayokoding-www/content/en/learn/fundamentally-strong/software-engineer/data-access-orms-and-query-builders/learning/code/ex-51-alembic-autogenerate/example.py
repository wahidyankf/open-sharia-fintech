# pyright: strict
"""Example 51: Autogenerate -- Deriving a Migration From a Model<->Schema Diff."""

from __future__ import annotations

import contextlib  # => co-20: swallows alembic's own non-deterministic scaffolding chatter, same reason as Example 48
import io  # => the throwaway buffer redirect_stdout writes that chatter INTO
import os  # => reads connection settings, and builds/removes the scratch project directory
import shutil  # => co-20: cleanup -- removes the scaffolded project directory once this example is done
import tempfile  # => co-20: a fresh, self-contained directory for the scaffolded migration project

from alembic import command  # => co-20: revision(autogenerate=True) is what DIFFS the models against the live schema
from alembic.config import Config  # => co-20: every alembic.command function needs one of these as its first argument
from sqlalchemy import create_engine, text  # => co-20: the live database autogenerate compares the models AGAINST
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # => co-20: the SAME Mapped[] models Examples 14-15 taught

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance


class Base(DeclarativeBase):  # => co-06: every mapped class in this program shares ONE DeclarativeBase
    pass  # => carries no columns -- purely a registry root


class Widget(Base):  # => co-20: exists ONLY in Python -- the database starts with NO widget table at all
    __tablename__ = "widget"  # => the physical table name autogenerate will propose creating
    id: Mapped[int] = mapped_column(primary_key=True)  # => auto-assigned by Postgres
    name: Mapped[str]  # => a required TEXT column


# => co-20: the SAME minimal env.py pattern from Examples 49-50, but `target_metadata` now reads a REAL MetaData
# => object -- autogenerate needs this to know what your models SAY the schema should look like
ENV_PY = (  # => co-20: built as SEPARATE joined string lines, so each line can carry its own comment
    "from alembic import context\n"  # => co-20: `context` is alembic's OWN migration-runtime handle
    "from sqlalchemy import engine_from_config, pool\n\n"  # => co-20: builds a real Engine straight from alembic.ini's own section
    "config = context.config\n"  # => co-20: the SAME Config object bootstrap() constructed, now read back inside env.py
    'target_metadata = config.attributes.get("target_metadata")\n\n\n'  # => co-20: THIS run sets it to Widget's own Base.metadata
    "def run_migrations_online() -> None:\n"  # => co-20: THE function alembic's runtime calls for a live-connection migration
    "    connectable = engine_from_config(\n"  # => co-20: reads the sqlalchemy.* keys straight out of alembic.ini's own section
    '        config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool\n'  # => no reuse needed
    "    )\n"  # => a short-lived migration run has no reason to KEEP a pooled connection open afterward
    "    with connectable.connect() as connection:\n"  # => borrows ONE connection -- autogenerate reflects THROUGH it
    "        context.configure(connection=connection, target_metadata=target_metadata)\n"  # => co-20: what autogenerate DIFFS against
    "        with context.begin_transaction():\n"  # => co-20: wraps every upgrade()/downgrade() call in ONE transaction
    "            context.run_migrations()\n\n\n"  # => the actual dispatch -- also used by autogenerate's own reflection pass
    "run_migrations_online()\n"  # => co-20: executed the MOMENT alembic imports this file -- no __main__ guard, by design
)


def bootstrap(url: str, project_dir: str, metadata: object) -> Config:  # => co-20: metadata drives WHAT autogenerate compares to
    script_dir = os.path.join(project_dir, "migrations")  # => alembic's convention -- a "migrations" subfolder
    cfg = Config(os.path.join(project_dir, "alembic.ini"))  # => co-20: the Config object every command function needs
    cfg.set_main_option("script_location", script_dir)  # => tells Config where the scaffolded files live
    cfg.set_main_option("sqlalchemy.url", url)  # => co-20: the ONE connection string every migration runs against
    with contextlib.redirect_stdout(io.StringIO()):  # => swallows "Creating directory ... done" -- path varies per run
        command.init(cfg, script_dir)  # => co-20: scaffolds env.py, script.py.mako, README, versions/ (Example 48)
    with open(os.path.join(script_dir, "env.py"), "w") as f:  # => co-20: OVERWRITES the scaffolded env.py with our own
        f.write(ENV_PY)  # => a hand-edit step, exactly like a real project's post-init setup
    cfg.attributes["target_metadata"] = metadata  # => co-20: passed to env.py via `config.attributes`, alembic's own escape hatch
    return cfg  # => ready for command.revision(autogenerate=True)


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, used both to reset the schema and inspect the migration
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- the database starts EMPTY, no widget yet
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema -- autogenerate compares Widget AGAINST this

    project_dir = tempfile.mkdtemp(prefix="alembic_ex51_")  # => a fresh, throwaway migration project for this example
    cfg = bootstrap(SQLA_URL, project_dir, Base.metadata)  # => co-20: Widget's OWN metadata is what gets diffed below

    with contextlib.redirect_stdout(io.StringIO()) as buf:  # => captures the "Generating ..." AND any diff summary text
        rev = command.revision(cfg, message="add widget", autogenerate=True, rev_id="0001")  # => co-20: THE diff step itself
    assert rev is not None and not isinstance(rev, list)  # => narrows the Union return type for pyright --strict below
    generated_body = open(rev.path).read()  # => co-20: reads back the FILE autogenerate actually wrote, not a guess
    print(f"contains create_table widget: {'create_table' in generated_body and 'widget' in generated_body}")
    assert "op.create_table(" in generated_body and "'widget'" in generated_body  # => Output: contains create_table widget: True
    assert "commands auto generated by Alembic" in generated_body  # => co-20: alembic's own marker, warning "please adjust!"
    _ = buf.getvalue()  # => discarded -- captured only to keep the demonstrated stdout deterministic, not for its own content
    # => co-20: autogenerate DIFFED the live (empty) database against Widget's Mapped[] columns and proposed the exact
    # => DDL needed to reconcile them -- but it is a PROPOSAL, not a guarantee: Example 52 shows a case autogenerate
    # => gets subtly wrong, which is why every autogenerated migration still needs a human review before it ships

    shutil.rmtree(project_dir)  # => cleanup -- this example's own throwaway project, not a real repository
    print("ex-51 OK")  # => Output: ex-51 OK
