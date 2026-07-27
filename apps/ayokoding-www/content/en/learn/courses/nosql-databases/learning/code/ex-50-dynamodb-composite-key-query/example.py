"""Example 50: DynamoDB Composite Key Query."""  # => co-22: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => co-22: boto3's dynamic resource/client factory has no stubs pinned -- Any is the honest, explicit type

import boto3  # => co-22: the official AWS SDK for Python
from boto3.dynamodb.conditions import Key  # => co-22: a typed helper for building KeyConditionExpressions safely


def get_local_dynamodb_resource() -> Any:  # => co-22: the higher-level "resource" API, more Pythonic than raw "client" calls
    """Return a boto3 DynamoDB resource pointed at a local dynamodb-local instance."""  # => documents the contract
    return boto3.resource(  # => co-22: same endpoint/credential pattern as Example 49, via the resource API
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="us-east-1",  # => the local dynamodb-local endpoint, no real AWS account needed
        aws_access_key_id="fake",
        aws_secret_access_key="fake",  # => dynamodb-local accepts any credentials
    )  # => closes the boto3.resource() call -- returns a high-level resource bound to the local endpoint


def create_orders_table(resource: Any) -> None:  # => co-22: a COMPOSITE key -- partition key PLUS a sort key
    """Create a table with a composite key: customer_id (partition) + order_ts (sort)."""  # => documents the contract
    client = resource.meta.client  # => the underlying low-level client, needed for list/delete/waiter calls
    if "Orders" in client.list_tables()["TableNames"]:  # => resets state -- this example is fully self-contained
        client.delete_table(TableName="Orders")  # => removes any leftover table from a prior run
        client.get_waiter("table_not_exists").wait(TableName="Orders")  # => blocks until the delete genuinely completes
    resource.create_table(  # => co-22: KeySchema with BOTH a HASH (partition) and a RANGE (sort) key
        TableName="Orders",  # => the table this whole composite-key example uses
        KeySchema=[  # => co-22: this is the composite key -- customer_id groups items, order_ts orders them within a group
            {"AttributeName": "customer_id", "KeyType": "HASH"},  # => co-22: the PARTITION key
            {"AttributeName": "order_ts", "KeyType": "RANGE"},  # => co-22: the SORT key, DynamoDB's term for a clustering column
        ],  # => closes the KeySchema list -- exactly one HASH + one RANGE, the composite key's two halves
        AttributeDefinitions=[  # => key attributes must be declared with their type up front
            {"AttributeName": "customer_id", "AttributeType": "S"},  # => S == string type, the partition key's type
            {"AttributeName": "order_ts", "AttributeType": "N"},  # => N == number, sorted numerically within the partition
        ],  # => closes the AttributeDefinitions list -- both key attributes declared
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => local-testing throughput
    )  # => closes the create_table() call -- the table now exists, though not yet necessarily ACTIVE
    client.get_waiter("table_exists").wait(TableName="Orders")  # => blocks until the table is genuinely ready for writes


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    resource = get_local_dynamodb_resource()  # => connects to the local dynamodb-local Docker container
    create_orders_table(resource)  # => sets up the fresh, empty Orders table
    table = resource.Table("Orders")  # => the high-level Table object the resource API works through

    for ts in [3, 1, 2]:  # => co-22: inserted deliberately OUT of sort-key order -- DynamoDB stores them sorted regardless
        table.put_item(Item={"customer_id": "cust-1", "order_ts": ts, "amount": ts * 10})  # => 3 items, all in the SAME partition

    response = table.query(  # => co-22: Query, scoped to a partition + a sort-key RANGE condition -- not a full scan
        KeyConditionExpression=Key("customer_id").eq("cust-1") & Key("order_ts").between(1, 3),  # => co-22: partition eq + sort-key range
    )  # => closes the query() call -- only cust-1's own partition, order_ts 1-3, ever gets scanned
    items = response["Items"]  # => the ordered items DynamoDB returned for this partition + range
    timestamps = [int(item["order_ts"]) for item in items]  # => extracts the sort-key values, in RETURN order
    assert timestamps == [1, 2, 3]  # => co-22: DynamoDB returns items ORDERED by the sort key within the partition, regardless of insert order
    print(f"Ordered order_ts values within partition cust-1: {timestamps}")  # => Output: Ordered order_ts values within partition cust-1: [1, 2, 3]


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
