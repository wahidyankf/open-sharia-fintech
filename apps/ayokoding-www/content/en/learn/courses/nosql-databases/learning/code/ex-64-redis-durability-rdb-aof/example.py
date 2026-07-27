"""Example 64: Redis Durability RDB vs. AOF."""  # => co-21: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import redis  # => co-21: redis-py, the official typed Python client


def configure_rdb(client: redis.Redis) -> None:  # => co-21: point-in-time SNAPSHOT persistence -- periodic, not per-write
    """Configure RDB snapshotting: save every 60s if at least 1 key changed."""  # => documents the contract, no runtime output
    client.config_set("appendonly", "no")  # => co-21: AOF OFF -- RDB is the ONLY persistence mechanism active
    client.config_set("save", "60 1")  # => co-21: RDB snapshot triggers every 60s if >=1 key changed -- a PERIODIC, not per-write, checkpoint


def configure_aof(client: redis.Redis) -> None:  # => co-21: an APPEND-ONLY log of every write -- durable per-write, at a cost
    """Configure AOF append-only persistence, fsynced every second."""  # => documents the contract, no runtime output
    client.config_set("appendonly", "yes")  # => co-21: AOF ON -- every write command is logged, not just periodic snapshots
    client.config_set("appendfsync", "everysec")  # => co-21: fsyncs the AOF log to disk once per second -- a bounded, tunable durability window


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = redis.Redis(host="localhost", port=6379, db=0)  # => connects to a local Valkey/Redis instance

    configure_rdb(client)  # => co-21: switches this instance to RDB-only persistence
    rdb_save_config = client.config_get("save")["save"]  # => reads back the ACTUAL configured save policy
    rdb_aof_config = client.config_get("appendonly")["appendonly"]  # => reads back the ACTUAL configured AOF state
    assert rdb_save_config == "60 1"  # => co-21: confirms the RDB snapshot policy genuinely took effect
    assert rdb_aof_config == "no"  # => co-21: confirms AOF is genuinely OFF in this configuration
    print(f"RDB config: save='{rdb_save_config}', appendonly='{rdb_aof_config}'")  # => Output: RDB config: save='60 1', appendonly='no'
    # => co-21: RDB's recovery window is UP TO the snapshot interval -- writes since the LAST snapshot
    # => are lost on an unclean restart or crash, a real, bounded data-loss window

    configure_aof(client)  # => co-21: switches this instance to AOF persistence
    aof_state = client.config_get("appendonly")["appendonly"]  # => reads back the ACTUAL configured AOF state
    aof_fsync = client.config_get("appendfsync")["appendfsync"]  # => reads back the ACTUAL configured fsync policy
    assert aof_state == "yes"  # => co-21: confirms AOF is genuinely ON in this configuration
    assert aof_fsync == "everysec"  # => co-21: confirms the fsync cadence genuinely took effect
    print(f"AOF config: appendonly='{aof_state}', appendfsync='{aof_fsync}'")  # => Output: AOF config: appendonly='yes', appendfsync='everysec'
    # => co-21: AOF's recovery window is bounded by the fsync cadence -- at MOST ~1 second of writes
    # => lost on a crash with appendfsync=everysec, a MUCH tighter window than RDB's, at the cost of
    # => more disk I/O per second and a larger on-disk log to replay on restart

    print("RDB: periodic snapshot, up-to-interval data-loss window. AOF: per-second fsync, up-to-~1s data-loss window, more I/O overhead")  # => Output line
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
