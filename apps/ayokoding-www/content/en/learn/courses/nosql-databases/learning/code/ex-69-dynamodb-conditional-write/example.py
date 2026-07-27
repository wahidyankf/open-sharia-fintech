"""Example 69: DynamoDB Conditional Write."""  # => co-27: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => co-27: boto3's dynamic resource/client factory has no stubs pinned -- Any is the honest, explicit type

import boto3  # => co-27: the official AWS SDK for Python
from botocore.exceptions import ClientError  # => co-27: ConditionalCheckFailedException surfaces as a ClientError subtype


def get_local_dynamodb_client() -> Any:  # => co-27: connects to amazon/dynamodb-local, the official local-testing Docker image
    """Return a boto3 DynamoDB client pointed at a local dynamodb-local instance."""  # => documents the contract
    return boto3.client(  # => co-27: same endpoint/credential pattern as prior DynamoDB examples
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="us-east-1",  # => the local dynamodb-local endpoint, no real AWS account needed
        aws_access_key_id="fake",
        aws_secret_access_key="fake",  # => dynamodb-local accepts any credentials
    )  # => closes the boto3.client() call -- returns a low-level DynamoDB client bound to the local endpoint


def setup_locks_table(client: Any) -> None:  # => co-27: a table this example owns exclusively
    """Create a dedicated table for this conditional-write demonstration."""  # => documents the contract, no runtime output
    if "ResourceLocks" in client.list_tables()["TableNames"]:  # => resets state -- this example is fully self-contained
        client.delete_table(TableName="ResourceLocks")  # => removes any leftover table from a prior run
        client.get_waiter("table_not_exists").wait(TableName="ResourceLocks")  # => blocks until the delete genuinely completes
    client.create_table(  # => a minimal, single-partition-key table
        TableName="ResourceLocks",  # => the table this whole conditional-write example uses
        KeySchema=[{"AttributeName": "resource_id", "KeyType": "HASH"}],  # => a single partition key -- one lock per resource_id
        AttributeDefinitions=[{"AttributeName": "resource_id", "AttributeType": "S"}],  # => S == string type, the partition key's type
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => local-testing throughput
    )  # => closes the create_table() call -- the table now exists, though not yet necessarily ACTIVE
    client.get_waiter("table_exists").wait(TableName="ResourceLocks")  # => blocks until the table is genuinely ready


def try_acquire_lock(client: Any, resource_id: str, holder: str) -> bool:  # => co-27: returns True if the conditional write succeeded
    """Attempt to acquire a lock via a conditional PutItem -- fails if the item already exists."""  # => documents the contract
    try:  # => catches ONLY the specific ConditionalCheckFailedException a failed condition raises
        client.put_item(  # => co-27: PutItem with a ConditionExpression -- a compare-and-set, not a plain write
            TableName="ResourceLocks",  # => the table this conditional write targets
            Item={"resource_id": {"S": resource_id}, "held_by": {"S": holder}},  # => the lock item this holder is attempting to claim
            ConditionExpression="attribute_not_exists(resource_id)",  # => co-27: succeeds ONLY if no item with this key exists yet
        )  # => closes the put_item() call -- raises ClientError if the condition fails
        return True  # => co-27: the condition held -- this holder genuinely acquired the lock
    except ClientError as exc:  # => co-27: DynamoDB raises this for a FAILED condition, among other error classes
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":  # => co-27: the SPECIFIC error a failed condition raises
            return False  # => co-27: correctly rejected -- another holder already owns this lock
        raise  # => any OTHER error class is a genuine, unexpected failure -- must not be silently swallowed


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = get_local_dynamodb_client()  # => connects to the local dynamodb-local Docker container
    setup_locks_table(client)  # => sets up the fresh, empty ResourceLocks table

    first_attempt = try_acquire_lock(client, "resource-42", "worker-1")  # => co-27: no existing item -- should succeed
    assert first_attempt is True  # => co-27: worker-1 genuinely acquired the lock, the condition held
    print(f"worker-1 acquires lock on resource-42: succeeded = {first_attempt}")  # => Output: worker-1 acquires lock on resource-42: succeeded = True

    second_attempt = try_acquire_lock(client, "resource-42", "worker-2")  # => co-27: the SAME key, now already held -- should FAIL
    assert second_attempt is False  # => co-27: worker-2's conditional write correctly failed -- ConditionalCheckFailedException was caught
    print(f"worker-2 attempts the SAME lock:       succeeded = {second_attempt} (ConditionalCheckFailedException)")  # => Output: worker-2 attempts the SAME lock:       succeeded = False (ConditionalCheckFailedException)

    current_holder = client.get_item(TableName="ResourceLocks", Key={"resource_id": {"S": "resource-42"}})["Item"]["held_by"]["S"]  # => confirms who ACTUALLY holds it
    assert current_holder == "worker-1"  # => co-27: worker-1's original write was NEVER overwritten by worker-2's failed attempt
    print(f"Confirmed lock holder: {current_holder} (worker-2's write never overwrote it)")  # => Output: Confirmed lock holder: worker-1 (worker-2's write never overwrote it)


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
