# pyright: strict
"""Example 48: alembic init -- Scaffolding a Migration Environment."""

from __future__ import annotations

import contextlib  # => co-19: redirects alembic's own console chatter, which embeds a NON-DETERMINISTIC temp path
import io  # => the throwaway buffer contextlib.redirect_stdout writes alembic's chatter INTO, instead of the real terminal
import os  # => reads connection settings, and builds/removes the scratch project directory
import shutil  # => co-19: cleanup -- removes the scaffolded project directory once this example is done
import tempfile  # => co-19: a fresh, self-contained directory for the scaffolded migration project

from alembic import command  # => co-19: the SAME Python API `alembic` init/revision/upgrade CLI commands call internally
from alembic.config import Config  # => co-19: a Config object is what EVERY alembic.command function needs as its first arg

if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    project_dir = tempfile.mkdtemp(prefix="alembic_ex48_")  # => co-19: a throwaway directory -- this example's own "repo root"
    script_dir = os.path.join(project_dir, "migrations")  # => co-19: alembic's convention -- a "migrations" subfolder
    ini_path = os.path.join(project_dir, "alembic.ini")  # => co-19: alembic.ini -- the CLI's own config file, generated below

    cfg = Config(ini_path)  # => co-19: this Config object IS what `alembic init` would populate from a real alembic.ini
    cfg.set_main_option("script_location", script_dir)  # => co-19: tells Config where the scaffolded files should land
    with contextlib.redirect_stdout(io.StringIO()):  # => swallows "Creating directory /tmp/xyz... done" -- path varies per run
        command.init(cfg, script_dir)  # => co-19: THE scaffolding step -- identical to running `alembic init migrations`

    created_files = sorted(os.listdir(script_dir))  # => co-19: what `alembic init` actually wrote to disk, read back fresh
    print(f"created files: {created_files}")  # => Output: created files: ['README', 'env.py', 'script.py.mako', 'versions']
    assert created_files == ["README", "env.py", "script.py.mako", "versions"]  # => co-19: the exact scaffold, every time
    # => co-19: env.py wires alembic to a real database connection and your models; script.py.mako is the TEMPLATE every
    # => new revision file is generated from; versions/ is where individual migration scripts accumulate over time

    versions_dir = os.path.join(script_dir, "versions")  # => co-19: the directory EVERY future migration script lands in
    print(f"versions is a directory: {os.path.isdir(versions_dir)}")  # => Output: versions is a directory: True
    print(f"versions starts empty: {os.listdir(versions_dir) == []}")  # => Output: versions starts empty: True
    assert os.path.isdir(versions_dir) and os.listdir(versions_dir) == []  # => co-19: a fresh project has NO migrations yet
    # => co-19: `alembic init` only scaffolds the ENVIRONMENT -- it writes no migration of its own; Example 49 writes
    # => the FIRST real migration into this exact versions/ directory, using the same Config + command API shown here

    shutil.rmtree(project_dir)  # => co-19: cleanup -- this example's own throwaway project, not a real repository
    print("ex-48 OK")  # => Output: ex-48 OK
