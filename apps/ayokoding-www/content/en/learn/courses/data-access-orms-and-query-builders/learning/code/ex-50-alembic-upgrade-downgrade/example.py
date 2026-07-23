# pyright: strict
"""Example 50: upgrade() Then downgrade() -- the Schema Round-Trips Back to Empty."""

from __future__ import annotations

import contextlib  # => co-19: swallows alembic's own non-deterministic scaffolding chatter, same reason as Example 48
import io  # => the throwaway buffer redirect_stdout writes that chatter INTO
import os  # => reads connection settings, and builds/removes the scratch project directory
import shutil  # => co-19: cleanup -- removes the scaffolded project directory once this example is done
import tempfile  # => co-19: a fresh, self-contained directory for the scaffolded migration project

from alembic import command  # => co-19: init/revision/upgrade/downgrade -- the same API the alembic CLI itself calls
from alembic.config import Config  # => co-19: every alembic.command function needs one of these as its first argument
from sqlalchemy import create_engine, inspect, text  # => co-21: inspect() confirms the schema at EACH point in the round trip

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance

# => co-19: the SAME minimal, deterministic env.py pattern Example 49 established -- no fileConfig(), no logging noise
ENV_PY = (  # => co-19: built as SEPARATE joined string lines, so each line can carry its own comment
    "from alembic import context\n"  # => co-19: `context` is alembic's OWN migration-runtime handle, not SQLAlchemy's
    "from sqlalchemy import engine_from_config, pool\n\n"  # => co-19: builds a real Engine straight from alembic.ini's own section
    "config = context.config\n"  # => co-19: the SAME Config object bootstrap() constructed, now read back inside env.py
    'target_metadata = config.attributes.get("target_metadata")\n\n\n'  # => None here -- this example writes migrations by hand
    "def run_migrations_online() -> None:\n"  # => co-19: THE function alembic's runtime calls for a live-connection migration
    "    connectable = engine_from_config(\n"  # => co-19: reads the sqlalchemy.* keys straight out of alembic.ini's own section
    '        config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool\n'  # => no reuse needed
    "    )\n"  # => a short-lived migration run has no reason to KEEP a pooled connection open afterward
    "    with connectable.connect() as connection:\n"  # => borrows ONE connection for the whole migration run
    "        context.configure(connection=connection, target_metadata=target_metadata)\n"  # => co-19: binds THIS run's connection
    "        with context.begin_transaction():\n"  # => co-19: wraps every upgrade()/downgrade() call in ONE transaction
    "            context.run_migrations()\n\n\n"  # => co-19: the actual dispatch -- calls upgrade()/downgrade() on each revision
    "run_migrations_online()\n"  # => co-19: executed the MOMENT alembic imports this file -- no __main__ guard, by design
)


def bootstrap(url: str, project_dir: str) -> Config:  # => co-19: init + env.py rewrite, shared setup for every Alembic example
    script_dir = os.path.join(project_dir, "migrations")  # => alembic's convention -- a "migrations" subfolder
    cfg = Config(os.path.join(project_dir, "alembic.ini"))  # => co-19: the Config object every command function needs
    cfg.set_main_option("script_location", script_dir)  # => tells Config where the scaffolded files live
    cfg.set_main_option("sqlalchemy.url", url)  # => co-19: the ONE connection string every migration runs against
    with contextlib.redirect_stdout(io.StringIO()):  # => swallows "Creating directory ... done" -- path varies per run
        command.init(cfg, script_dir)  # => co-19: scaffolds env.py, script.py.mako, README, versions/ (Example 48)
    with open(os.path.join(script_dir, "env.py"), "w") as f:  # => co-19: OVERWRITES the scaffolded env.py with our own
        f.write(ENV_PY)  # => a hand-edit step, exactly like a real project's post-init setup
    return cfg  # => ready for command.revision()/upgrade()/downgrade() calls


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    engine = create_engine(SQLA_URL)  # => an ORM-capable engine, used both to reset the schema and to inspect it later
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema -- alembic's migration builds INTO this

    project_dir = tempfile.mkdtemp(prefix="alembic_ex50_")  # => a fresh, throwaway migration project for this example
    # => the round trip below is exactly what a CI job or a local `alembic upgrade head && alembic downgrade base` proves
    cfg = bootstrap(SQLA_URL, project_dir)  # => scaffolds + rewires env.py, matching Examples 48-49's own setup

    with contextlib.redirect_stdout(io.StringIO()):  # => swallows "Generating .../0001_create_widget.py ... done"
        rev = command.revision(cfg, message="create widget table", rev_id="0001")  # => co-19: an EMPTY skeleton
    assert rev is not None and not isinstance(rev, list)  # => narrows the Union return type for pyright --strict below
    with open(rev.path, "w") as f:  # => co-21: a REAL, REVERSIBLE migration -- upgrade() and downgrade() are TRUE inverses
        f.write(  # => the same create-table/drop-table pair from Example 49, reused here for the round-trip
            '"""create widget table"""\n'  # => the migration's own docstring -- what `alembic history` displays per revision
            "from typing import Sequence, Union\n"  # => typed to match what command.revision()'s own skeleton generates
            "from alembic import op\n"  # => co-19: `op` is alembic's schema-editing API
            "import sqlalchemy as sa\n\n"  # => column TYPES (sa.Integer, sa.String) for the create_table() call below
            'revision: str = "0001"\n'  # => co-19: THIS revision's own id -- matches the rev_id passed to command.revision()
            "down_revision: Union[str, Sequence[str], None] = None\n"  # => None -- this is the FIRST revision, nothing before it
            "branch_labels: Union[str, Sequence[str], None] = None\n"  # => unused here -- relevant only for branching histories
            "depends_on: Union[str, Sequence[str], None] = None\n\n"  # => unused here -- cross-branch dependency declarations
            "def upgrade() -> None:\n"  # => co-19: the FORWARD direction -- what `alembic upgrade head` runs
            '    op.create_table("widget", sa.Column("id", sa.Integer, primary_key=True), sa.Column("name", sa.String, nullable=False))\n\n'  # => DDL
            "def downgrade() -> None:\n"  # => co-21: the REVERSE direction -- what THIS example proves actually undoes the upgrade
            '    op.drop_table("widget")\n'  # => co-21: a TRUE inverse -- no data or structure survives that upgrade() didn't add
        )

    with contextlib.redirect_stdout(io.StringIO()):  # => swallows alembic's own noisy status lines
        command.upgrade(cfg, "head")  # => co-19: STEP 1 of the round trip -- runs upgrade(), the schema now has `widget`
    tables_up = sorted(inspect(engine).get_table_names())  # => co-21: reads Postgres' OWN catalog right after upgrading
    print(f"tables after upgrade: {tables_up}")  # => Output: tables after upgrade: ['alembic_version', 'widget']
    assert tables_up == ["alembic_version", "widget"]  # => co-19: the forward direction landed correctly

    with contextlib.redirect_stdout(io.StringIO()):  # => swallows alembic's own noisy status lines
        command.downgrade(cfg, "base")  # => co-21: STEP 2 of the round trip -- runs downgrade(), back to the START
    tables_down = sorted(inspect(create_engine(SQLA_URL)).get_table_names())  # => co-21: a FRESH inspector, no stale cache
    print(f"tables after downgrade: {tables_down}")  # => Output: tables after downgrade: ['alembic_version']
    assert tables_down == ["alembic_version"]  # => co-21: `widget` is GONE -- only alembic's own tracking table remains
    # => a migration that DOESN'T survive this round trip is a common source of "works on my machine" schema drift
    # => co-21: "base" means "no migrations applied" -- the schema is now back to where it started, MINUS alembic_version
    # => itself, which alembic keeps around even at base to remember it once managed this database at all

    shutil.rmtree(project_dir)  # => cleanup -- this example's own throwaway project, not a real repository
    print("ex-50 OK")  # => Output: ex-50 OK
