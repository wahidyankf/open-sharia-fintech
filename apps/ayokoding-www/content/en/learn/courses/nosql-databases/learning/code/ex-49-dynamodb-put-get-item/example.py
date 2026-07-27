"""Example 49: DynamoDB put_item/get_item."""  # => co-22: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => co-22: boto3's dynamic resource/client factory has no stubs pinned -- Any is the honest, explicit type

import boto3  # => co-22: the official AWS SDK for Python -- talks to real DynamoDB or amazon/dynamodb-local identically


def get_local_dynamodb_client() -> Any:  # => co-22: connects to amazon/dynamodb-local, the official local-testing Docker image
    """Return a boto3 DynamoDB client pointed at a local dynamodb-local instance."""  # => documents the contract
    return boto3.client(  # => co-22: same boto3 API surface as real AWS -- only the endpoint_url differs
        "dynamodb",  # => the service name -- boto3 resolves this to DynamoDB's own API model at runtime
        endpoint_url="http://localhost:8000",  # => co-22: amazon/dynamodb-local listens here, no real AWS account needed
        region_name="us-east-1",  # => a region is required by the SDK even though dynamodb-local ignores it
        aws_access_key_id="fake",  # => co-22: dynamodb-local accepts any credentials -- no real AWS auth involved
        aws_secret_access_key="fake",  # => co-22: same -- purely local, no network call ever leaves this machine
    )  # => closes the boto3.client() call -- returns a low-level DynamoDB client bound to the local endpoint


def create_table(client: Any) -> None:  # => co-22: a minimal single-key table -- partition key only, no sort key yet
    """Create a table keyed by a simple partition key (user_id), deleting any prior copy first."""  # => documents contract
    existing = client.list_tables()["TableNames"]  # => checks what already exists, for idempotent re-runs
    if "Users" in existing:  # => resets state -- this example is fully self-contained
        client.delete_table(TableName="Users")  # => co-22: removes any leftover table from a prior run
        client.get_waiter("table_not_exists").wait(TableName="Users")  # => blocks until the delete genuinely completes
    client.create_table(  # => co-22: PROVISIONED billing mode for dynamodb-local's default test setup
        TableName="Users",  # => the table this whole example operates against
        KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],  # => co-22: HASH == the partition key, DynamoDB's own term
        AttributeDefinitions=[{"AttributeName": "user_id", "AttributeType": "S"}],  # => S == string type
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => local-testing throughput, ignored by dynamodb-local's billing
    )  # => closes the create_table() call -- the table now exists, though not yet necessarily ACTIVE
    client.get_waiter("table_exists").wait(TableName="Users")  # => blocks until the table is genuinely ready for writes


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = get_local_dynamodb_client()  # => connects to the local dynamodb-local Docker container
    create_table(client)  # => sets up the fresh, empty Users table

    client.put_item(  # => co-22: PutItem writes a whole item, keyed by the partition key
        TableName="Users",  # => the table receiving this item
        Item={"user_id": {"S": "user-1"}, "name": {"S": "Ada"}, "role": {"S": "engineer"}},  # => co-22: DynamoDB's typed attribute-value wire format
    )  # => closes the put_item() call -- the item is now durably stored under partition key user-1
    response = client.get_item(TableName="Users", Key={"user_id": {"S": "user-1"}})  # => co-22: GetItem reads by the SAME partition key
    item = response["Item"]  # => the raw typed item DynamoDB returned
    assert item["name"]["S"] == "Ada"  # => co-22: the round trip returned exactly what was written
    assert item["role"]["S"] == "engineer"  # => confirms every attribute survived the round trip intact
    print(f"Round trip on partition key user_id=user-1: name={item['name']['S']}, role={item['role']['S']}")  # => Output: Round trip on partition key user_id=user-1: name=Ada, role=engineer


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
