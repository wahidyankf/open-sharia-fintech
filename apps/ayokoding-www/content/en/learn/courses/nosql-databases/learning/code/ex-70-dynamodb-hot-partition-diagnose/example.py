"""Example 70: DynamoDB Hot Partition Diagnosis."""  # => co-10: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from collections import Counter  # => co-10: tallies how many items land under each distinct partition key value
from typing import Any  # => co-10: boto3's dynamic resource/client factory has no stubs pinned -- Any is the honest, explicit type

import boto3  # => co-10: the official AWS SDK for Python


def get_local_dynamodb_resource() -> Any:  # => co-10: the higher-level "resource" API
    """Return a boto3 DynamoDB resource pointed at a local dynamodb-local instance."""  # => documents the contract
    return boto3.resource(  # => co-10: same endpoint/credential pattern as prior DynamoDB examples
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="us-east-1",  # => the local dynamodb-local endpoint, no real AWS account needed
        aws_access_key_id="fake",
        aws_secret_access_key="fake",  # => dynamodb-local accepts any credentials
    )  # => closes the boto3.resource() call -- returns a high-level resource bound to the local endpoint


def create_events_table(resource: Any) -> None:  # => co-10: a table this example owns exclusively
    """Create a dedicated table for this hot-partition-key demonstration."""  # => documents the contract, no runtime output
    client = resource.meta.client  # => the underlying low-level client, needed for list/delete/waiter calls
    if "EventsSkew" in client.list_tables()["TableNames"]:  # => resets state -- this example is fully self-contained
        client.delete_table(TableName="EventsSkew")  # => removes any leftover table from a prior run
        client.get_waiter("table_not_exists").wait(TableName="EventsSkew")  # => blocks until the delete genuinely completes
    resource.create_table(  # => a minimal table keyed by whatever partition_key value the caller provides
        TableName="EventsSkew",  # => the table this whole hot-partition example uses
        KeySchema=[{"AttributeName": "partition_key", "KeyType": "HASH"}, {"AttributeName": "event_id", "KeyType": "RANGE"}],  # => partition key + sort key, the pair this example varies
        AttributeDefinitions=[{"AttributeName": "partition_key", "AttributeType": "S"}, {"AttributeName": "event_id", "AttributeType": "S"}],  # => both attributes are string-typed
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => local-testing throughput
    )  # => closes the create_table() call -- the table now exists, though not yet necessarily ACTIVE
    client.get_waiter("table_exists").wait(TableName="EventsSkew")  # => blocks until the table is genuinely ready


def load_with_skewed_key(table: Any) -> Counter[str]:  # => co-10: a SINGLE, coarse partition key -- date-only, no per-user distinction
    """Load 100 events under a coarse date-only partition key -- ALL traffic concentrates on ONE partition."""  # => documents contract
    for i in range(100):  # => co-10: 100 events, ALL on "2026-07-27" -- a poor choice of partition key granularity
        table.put_item(Item={"partition_key": "2026-07-27", "event_id": str(i), "user": f"user-{i % 10}"})  # => co-10: coarse date-only key
    scan = table.scan()  # => reads every item back to inspect its ACTUAL partition key
    return Counter(item["partition_key"] for item in scan["Items"])  # => co-10: counts how many items landed under each distinct partition key


def load_with_composite_key(table: Any) -> Counter[str]:  # => co-10: a MORE SELECTIVE composite key -- date PLUS user id
    """Load the SAME 100 events under a composite date+user partition key -- traffic spreads across 10 partitions."""  # => documents contract
    for i in range(100):  # => co-10: the SAME 100 logical events, keyed MORE SELECTIVELY this time
        table.put_item(Item={"partition_key": f"2026-07-27#user-{i % 10}", "event_id": str(i), "user": f"user-{i % 10}"})  # => co-10: composite key spreads load
    scan = table.scan()  # => reads every item back to inspect its ACTUAL partition key
    return Counter(item["partition_key"] for item in scan["Items"] if item["partition_key"].startswith("2026-07-27#"))  # => co-10: counts per distinct composite key


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    resource = get_local_dynamodb_resource()  # => connects to the local dynamodb-local Docker container
    create_events_table(resource)  # => sets up the fresh, empty EventsSkew table
    table = resource.Table("EventsSkew")  # => the high-level Table object the resource API works through

    skewed_distribution = load_with_skewed_key(table)  # => co-10: loads 100 items under ONE coarse key
    max_skewed_partition_size = max(skewed_distribution.values())  # => co-10: the SINGLE most-loaded partition's item count
    assert len(skewed_distribution) == 1  # => co-10: only ONE distinct partition key exists -- ALL 100 items concentrate there
    assert max_skewed_partition_size == 100  # => co-10: a genuinely HOT partition -- every write and read hits the same physical partition
    print(f"Skewed key: {len(skewed_distribution)} distinct partition(s), max load = {max_skewed_partition_size} items")  # => Output: Skewed key: 1 distinct partition(s), max load = 100 items

    composite_distribution = load_with_composite_key(table)  # => co-10: loads the SAME 100 items under a more selective key
    max_composite_partition_size = max(composite_distribution.values())  # => co-10: the SINGLE most-loaded composite partition's item count
    assert len(composite_distribution) == 10  # => co-10: 10 distinct partitions -- ONE per user id, the load genuinely spread
    assert max_composite_partition_size == 10  # => co-10: each partition holds only 10 of the 100 items -- 10x LESS concentrated
    print(f"Composite key: {len(composite_distribution)} distinct partition(s), max load = {max_composite_partition_size} items")  # => Output: Composite key: 10 distinct partition(s), max load = 10 items

    assert max_composite_partition_size < max_skewed_partition_size  # => co-10: verifies the improvement directly -- the hot spot genuinely diffused
    print(
        f"A more selective composite key reduced the single-partition load from {max_skewed_partition_size} to {max_composite_partition_size} items"
    )  # => Output: A more selective composite key reduced the single-partition load from 100 to 10 items


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
