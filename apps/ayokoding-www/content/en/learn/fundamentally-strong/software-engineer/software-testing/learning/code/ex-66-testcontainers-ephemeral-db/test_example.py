"""Example 66: Spin Up a Throwaway DB Container for a Test, Then Verify Teardown."""
# This is a REAL Docker container, started and torn down by the actual Docker daemon -- the
# final assertion below shells out to `docker ps -a` to prove teardown genuinely happened.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

import subprocess  # => co-25: shells into the REAL container -- no Postgres driver library needed  # fmt: skip

import pytest  # => co-08: marks this test as needing Docker  # fmt: skip
from testcontainers.core.container import DockerContainer  # => co-25: real Docker, real container  # fmt: skip
from testcontainers.core.wait_strategies import (
    LogMessageWaitStrategy,
)  # => a structured readiness wait


def _pg_isready(
    container_id: str,
) -> subprocess.CompletedProcess[str]:  # => shells INTO the real container
    return subprocess.run(  # => co-25: `docker exec` against the ACTUAL running container, not a mock  # fmt: skip
        [
            "docker",
            "exec",
            container_id,
            "pg_isready",
            "-U",
            "postgres",
        ],  # => the real health-check command  # fmt: skip
        capture_output=True,  # => captures stdout/stderr for the assertion below  # fmt: skip
        text=True,  # => decodes output as str, not bytes  # fmt: skip
        timeout=10,  # => fails fast if the real container never responds  # fmt: skip
    )


def _container_still_exists(
    container_id: str,
) -> bool:  # => checks Docker's OWN bookkeeping, post-teardown
    listing = subprocess.run(  # => `docker ps -a` sees stopped-but-not-removed containers too  # fmt: skip
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            f"id={container_id}",
            "--format",
            "{{.ID}}",
        ],  # => filter by id  # fmt: skip
        capture_output=True,  # => captures the listing's stdout  # fmt: skip
        text=True,  # => decodes output as str  # fmt: skip
        timeout=10,  # => fails fast, never hangs the test  # fmt: skip
    )
    return listing.stdout.strip() != ""  # => non-empty output means Docker still knows about it  # fmt: skip


@pytest.mark.integration  # => co-08/co-10: this test needs Docker -- a real, marked integration test  # fmt: skip
def test_ephemeral_postgres_is_created_and_torn_down() -> None:  # => co-25: the ONE test in this file  # fmt: skip
    container = DockerContainer("postgres:17-alpine")  # => co-25: a REAL, throwaway Postgres image  # fmt: skip
    container.with_env("POSTGRES_PASSWORD", "scratch")  # => the ONE env var this image requires  # fmt: skip
    container.with_exposed_ports(
        5432
    )  # => Postgres's own well-known port, published to a random host port
    container.waiting_for(  # => co-25: blocks start() until the DB genuinely finishes initializing  # fmt: skip
        LogMessageWaitStrategy(
            "database system is ready to accept connections"
        )  # => the REAL readiness line  # fmt: skip
    )

    with container:  # => co-25: `with` starts the REAL container, and tears it down on block exit  # fmt: skip
        container_id = container.get_wrapped_container().id  # => the genuine Docker container id  # fmt: skip
        ready = _pg_isready(container_id)  # => a REAL health check run INSIDE the REAL container  # fmt: skip
        assert ready.returncode == 0  # => confirms Postgres genuinely accepted the readiness check  # fmt: skip
        assert "accepting connections" in ready.stdout  # => the REAL pg_isready message, not asserted-away  # fmt: skip
        assert _container_still_exists(container_id)  # => confirms it's ACTUALLY running right now  # fmt: skip

    # co-25: outside the `with` block, testcontainers has ALREADY stopped and removed the container --
    # this is the "torn down around the run" half of ex-66's verify criterion, checked for real below.
    assert not _container_still_exists(container_id)  # => Docker itself confirms it's genuinely gone  # fmt: skip
