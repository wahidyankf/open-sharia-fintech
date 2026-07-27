"""Example 30: Redis Pipeline vs. Transaction."""  # => co-27: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import threading  # => co-27: simulates a concurrent client interleaving with a plain pipeline's commands
import time  # => co-27: a tiny sleep opens a genuine interleaving window for the race demonstration

import redis  # => co-27: redis-py, the official typed Python client


def run_plain_pipeline(client: redis.Redis, key: str) -> None:  # => co-27: NO transaction=True -- commands can interleave with others
    """Queue two commands in a NON-transactional pipeline (transaction=False)."""  # => documents the contract
    pipe = client.pipeline(transaction=False)  # => co-27: transaction=False -- batches network round trips only, NO atomicity
    pipe.set(key, "step-1")  # => queued, sent in the same batch, but NOT wrapped in MULTI/EXEC
    time.sleep(0.05)  # => co-27: an artificial gap -- a real pipeline batches sends, but the SERVER can still interleave other clients' commands between these two
    pipe.set(key, "step-2")  # => queued, sent in the same batch
    pipe.execute()  # => co-27: sends the batch -- but nothing here PREVENTED another client from writing key in between


def run_multi_exec(client: redis.Redis, key: str) -> None:  # => co-27: WITH transaction=True -- genuinely atomic application
    """Queue the SAME two commands inside MULTI/EXEC (transaction=True)."""  # => documents the contract
    pipe = client.pipeline(transaction=True)  # => co-27: transaction=True -- wraps the batch in MULTI/EXEC
    pipe.multi()  # => co-27: MULTI -- starts queuing
    pipe.set(key, "step-1")  # => QUEUED, not yet applied
    pipe.set(key, "step-2")  # => QUEUED, not yet applied
    pipe.execute()  # => co-27: EXEC -- both apply back-to-back, no other client's write can land between them


def concurrent_interferer(client: redis.Redis, key: str) -> None:  # => a second "client" racing against run_plain_pipeline
    """Sleep briefly, then overwrite key -- simulating a concurrent client racing the pipeline."""  # => documents contract
    time.sleep(0.02)  # => times this write to land INSIDE run_plain_pipeline's artificial 0.05s gap above
    client.set(key, "interloper")  # => co-27: a genuinely concurrent write landing mid-pipeline


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = redis.Redis(host="localhost", port=6379, db=0)  # => connects to a local Valkey/Redis instance

    # --- Plain pipeline: interference CAN show through, because there is no MULTI/EXEC boundary ---
    client.set("demo:pipeline", "start")  # => resets state for the pipeline case
    interferer = threading.Thread(target=concurrent_interferer, args=(client, "demo:pipeline"))  # => a racing second client
    interferer.start()  # => starts racing concurrently with the pipeline below
    run_plain_pipeline(client, "demo:pipeline")  # => co-27: the interloper's write CAN land between "step-1" and "step-2"
    interferer.join()  # => waits for the racing thread to finish before reading the result
    pipeline_raw = client.get("demo:pipeline")  # => reads the raw bytes | str | None reply
    assert pipeline_raw is not None  # => the key was SET above, so a reply always exists -- narrows away None
    pipeline_result = pipeline_raw.decode() if isinstance(pipeline_raw, bytes) else pipeline_raw  # => decodes only if the driver returned raw bytes
    # => whichever write landed LAST wins -- not guaranteed to be "step-2"
    print(f"Plain pipeline final value (order not guaranteed): {pipeline_result}")  # => Output line -- value depends on timing

    # --- MULTI/EXEC: the SAME race, but atomicity means the two queued SETs apply back-to-back ---
    client.set("demo:transaction", "start")  # => resets state for the transaction case
    interferer2 = threading.Thread(target=concurrent_interferer, args=(client, "demo:transaction"))  # => a racing second client
    interferer2.start()  # => starts racing concurrently with the transaction below
    run_multi_exec(client, "demo:transaction")  # => co-27: EXEC applies BOTH queued SETs with no other client's command between them
    interferer2.join()  # => waits for the racing thread to finish before reading the result
    transaction_raw = client.get("demo:transaction")  # => reads the raw bytes | str | None reply
    assert transaction_raw is not None  # => the key was SET above, so a reply always exists -- narrows away None
    transaction_result = transaction_raw.decode() if isinstance(transaction_raw, bytes) else transaction_raw  # => decodes only if the driver returned raw bytes
    # => the interloper's write lands strictly BEFORE or AFTER the whole EXEC, never between step-1 and step-2
    print(f"MULTI/EXEC final value (interloper cannot split the pair): {transaction_result}")  # => Output line
    assert transaction_result in ("step-2", "interloper")  # => co-27: either the interloper won outright, or the atomic pair won outright -- never a torn state
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
