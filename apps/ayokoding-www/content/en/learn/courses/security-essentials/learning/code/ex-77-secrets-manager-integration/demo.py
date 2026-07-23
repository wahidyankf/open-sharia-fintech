# learning/code/ex-77-secrets-manager-integration/demo.py
"""Example 77: fetches a secret at RUNTIME from the manager stand-in -- never from code, and rotates with no redeploy (co-17)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the demo logic itself

import secrets  # => co-17: cryptographically random secret VALUES -- generated fresh, never hardcoded anywhere
import tempfile  # => co-17: a genuinely throwaway, real on-disk location for the stand-in's store file
from pathlib import (
    Path,
)  # => co-17: real filesystem paths for both the store file and this example's own source

from secrets_manager import (
    FileBackedSecretsManager,
)  # => co-17: this example's real, file-backed stand-in

HERE = (
    Path(__file__).parent
)  # => co-17: this example's own real source directory -- what the grep check sweeps


def fetch_db_password(
    manager: FileBackedSecretsManager,
) -> str:  # => co-17: simulates a REAL app's runtime fetch
    # => co-17: this function NEVER reads an env var, NEVER imports a constant -- it asks the
    # => manager, AT CALL TIME, exactly like a real app would ask AWS Secrets Manager or Vault
    return manager.get_secret(
        "db_password"
    )  # => co-17: the ONE real call this whole example's security rests on


def main() -> (
    None
):  # => co-17: seeds a real secret, fetches it, greps for leaks, rotates it, fetches again
    store_path = (
        Path(tempfile.mkdtemp(prefix="ex77-secrets-")) / "store.json"
    )  # => co-17: REAL, outside this source tree
    manager = FileBackedSecretsManager(
        store_path
    )  # => co-17: a real, fresh stand-in instance for this run

    print(
        "=== seeding the initial secret (a real ops/deploy-time action, not a code change) ==="
    )  # => labels section
    initial_password = secrets.token_urlsafe(
        24
    )  # => co-17: a REAL, randomly generated secret value
    manager.rotate_secret(
        "db_password", initial_password
    )  # => co-17: the real, first write to the stand-in's store
    print(
        f"seeded (value never printed in full): {initial_password[:6]}..."
    )  # => co-17: real, deliberately truncated

    print("\n=== the app fetches the secret at RUNTIME ===")  # => labels section
    fetched_1 = fetch_db_password(
        manager
    )  # => co-17: a REAL runtime fetch -- this is the ONLY place the value flows
    print(
        f"fetched: {fetched_1[:6]}... matches seeded value: {fetched_1 == initial_password}"
    )  # => co-17: real check
    assert (
        fetched_1 == initial_password
    )  # => co-17: proves the real fetch returns the real, currently-stored value

    print(
        "\n=== verifying NO secret value appears anywhere in this example's own source tree ==="
    )  # => labels section
    source_files = sorted(
        HERE.glob("*.py")
    )  # => co-17: every REAL .py file that ships with this example
    for source_file in source_files:  # => co-17: sweeps EVERY real file, not a sample
        text = (
            source_file.read_text()
        )  # => co-17: the REAL, on-disk source text of this file
        assert (
            initial_password not in text
        )  # => co-17: proves the REAL secret value never landed in committed code
        print(f"  {source_file.name}: clean")  # => co-17: real, per-file confirmation

    print(
        "\n=== rotating the secret (a real ops action) -- NO code change, NO redeploy ==="
    )  # => labels section
    rotated_password = secrets.token_urlsafe(
        24
    )  # => co-17: a REAL, freshly generated replacement value
    manager.rotate_secret(
        "db_password", rotated_password
    )  # => co-17: the REAL rotation -- mutates only the store file
    fetched_2 = fetch_db_password(
        manager
    )  # => co-17: the SAME real fetch function, no code changed since fetched_1
    print(
        f"fetched after rotation: {fetched_2[:6]}..."
    )  # => co-17: real, deliberately truncated
    assert (
        fetched_2 == rotated_password
    )  # => co-17: proves the NEXT fetch really returns the NEW value
    assert (
        fetched_2 != fetched_1
    )  # => co-17: proves rotation really took effect -- the two real fetches genuinely differ


if (
    __name__ == "__main__"
):  # => co-17: only runs when launched directly, e.g. `python3 demo.py`
    main()  # => co-17: runs the full real seed -> fetch -> grep -> rotate -> re-fetch sequence
