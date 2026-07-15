# learning/code/ex-77-secrets-manager-integration/secrets_manager.py
"""Example 77: a real, file-backed secrets-manager STAND-IN -- an HONEST substitute for AWS Secrets Manager/Vault (co-17)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the stand-in interface itself

import json  # => co-17: the real, on-disk serialization this stand-in's store actually uses
from pathlib import (
    Path,
)  # => co-17: real filesystem paths -- the store lives OUTSIDE this example's own source tree

# => co-17: HONEST LIMITATION -- a real cloud secrets vault isn't available in this sandbox. The class
# => below matches the INTERFACE SHAPE (get_secret(name) -> value, with rotation taking effect
# => immediately, no redeploy) of two REAL production services, whose actual call shapes are:
# =>   AWS Secrets Manager: boto3.client("secretsmanager").get_secret_value(SecretId=name)["SecretString"]
# =>   HashiCorp Vault (KV v2): hvac.Client(url=...).secrets.kv.v2.read_secret_version(path=name)["data"]["data"]
# => Both of THOSE are real network calls to a managed service with its own access control and audit
# => log; this stand-in is a LOCAL FILE for self-containment only, not a claim of equal security.


class FileBackedSecretsManager:  # => co-17: a real, minimal get_secret(name) interface -- the shape any caller needs
    def __init__(
        self, store_path: Path
    ) -> None:  # => co-17: takes a REAL, on-disk path -- never inside source control
        self.store_path = (
            store_path  # => co-17: the real file this manager's state actually lives in
        )
        if (
            not self.store_path.exists()
        ):  # => co-17: real, idempotent first-run initialization
            self.store_path.write_text(
                "{}"
            )  # => co-17: a real, empty JSON object -- no secrets yet

    def get_secret(
        self, name: str
    ) -> str:  # => co-17: the ONE real method every caller uses to fetch a secret VALUE
        store = json.loads(
            self.store_path.read_text()
        )  # => co-17: re-reads the REAL file fresh on EVERY call
        # => co-17: re-reading on every call (rather than caching at import time) is exactly what
        # => makes rotation take effect immediately -- the SAME as a real vault's get call
        if (
            name not in store
        ):  # => co-17: a real guard -- no such secret has ever been set
            raise KeyError(
                f"no such secret: {name!r}"
            )  # => co-17: a real, named failure
        return store[
            name
        ]  # => co-17: the REAL, CURRENT value -- never a cached or stale copy

    def rotate_secret(
        self, name: str, new_value: str
    ) -> None:  # => co-17: the REAL operator/rotation action
        store = json.loads(
            self.store_path.read_text()
        )  # => co-17: reads the real, current state before mutating it
        store[name] = (
            new_value  # => co-17: the REAL, in-memory update -- not yet persisted
        )
        self.store_path.write_text(
            json.dumps(store)
        )  # => co-17: persists the REAL, rotated value to disk immediately
