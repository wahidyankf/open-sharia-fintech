"""Example 51: DynamoDB Single-Table Two Entities."""  # => co-23: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => co-23: boto3's dynamic resource/client factory has no stubs pinned -- Any is the honest, explicit type

import boto3  # => co-23: the official AWS SDK for Python
from boto3.dynamodb.conditions import Key  # => co-23: a typed helper for building KeyConditionExpressions safely


def get_local_dynamodb_resource() -> Any:  # => co-23: the higher-level "resource" API
    """Return a boto3 DynamoDB resource pointed at a local dynamodb-local instance."""  # => documents the contract
    return boto3.resource(  # => co-23: same endpoint/credential pattern as prior DynamoDB examples
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="us-east-1",  # => the local dynamodb-local endpoint, no real AWS account needed
        aws_access_key_id="fake",
        aws_secret_access_key="fake",  # => dynamodb-local accepts any credentials
    )  # => closes the boto3.resource() call -- returns a high-level resource bound to the local endpoint


def create_single_table(resource: Any) -> None:  # => co-23: ONE table, sort key will carry overloaded entity-type prefixes
    """Create a single table with a generic PK/SK composite key, ready to hold multiple entity types."""  # => documents contract
    client = resource.meta.client  # => the underlying low-level client, needed for list/delete/waiter calls
    if "AppTable" in client.list_tables()["TableNames"]:  # => resets state -- this example is fully self-contained
        client.delete_table(TableName="AppTable")  # => removes any leftover table from a prior run
        client.get_waiter("table_not_exists").wait(TableName="AppTable")  # => blocks until the delete genuinely completes
    resource.create_table(  # => co-23: deliberately GENERIC attribute names -- "PK"/"SK" carry no entity-specific meaning
        TableName="AppTable",  # => the ONE table this whole single-table-design example uses
        KeySchema=[{"AttributeName": "PK", "KeyType": "HASH"}, {"AttributeName": "SK", "KeyType": "RANGE"}],  # => co-23: single-table design's signature generic key
        AttributeDefinitions=[{"AttributeName": "PK", "AttributeType": "S"}, {"AttributeName": "SK", "AttributeType": "S"}],  # => both key attributes are plain strings
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => local-testing throughput
    )  # => closes the create_table() call -- the table now exists, though not yet necessarily ACTIVE
    client.get_waiter("table_exists").wait(TableName="AppTable")  # => blocks until the table is genuinely ready for writes


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    resource = get_local_dynamodb_resource()  # => connects to the local dynamodb-local Docker container
    create_single_table(resource)  # => sets up the fresh, empty AppTable
    table = resource.Table("AppTable")  # => the high-level Table object the resource API works through

    # Entity type 1: a customer PROFILE, sort key prefixed "PROFILE" -- co-23's overloaded sort-key pattern.
    table.put_item(Item={"PK": "CUSTOMER#42", "SK": "PROFILE", "name": "Ada", "type": "profile"})  # => co-23: entity 1 under the SAME partition key
    # Entity type 2: two of that SAME customer's ORDERS, sort key prefixed "ORDER#" -- a DIFFERENT entity type, SAME partition.
    table.put_item(Item={"PK": "CUSTOMER#42", "SK": "ORDER#2026-01", "amount": 50, "type": "order"})  # => co-23: entity 2, first order
    table.put_item(Item={"PK": "CUSTOMER#42", "SK": "ORDER#2026-02", "amount": 75, "type": "order"})  # => co-23: entity 2, second order

    response = table.query(KeyConditionExpression=Key("PK").eq("CUSTOMER#42"))  # => co-23: ONE query retrieves BOTH entity types under this partition
    items = response["Items"]  # => every item under CUSTOMER#42, regardless of entity type
    types_found = sorted({item["type"] for item in items})  # => co-23: distinct entity types retrieved by this SINGLE query
    assert types_found == ["order", "profile"]  # => co-23: both entity types retrievable under the SAME partition key, no second table/query needed
    assert len(items) == 3  # => co-23: 1 profile + 2 orders, all under one partition, one query
    print(f"Entity types under CUSTOMER#42 (single query): {types_found}, {len(items)} total items")  # => Output: Entity types under CUSTOMER#42 (single query): ['order', 'profile'], 3 total items


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
