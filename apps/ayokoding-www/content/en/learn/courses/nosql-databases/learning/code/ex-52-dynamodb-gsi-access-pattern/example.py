"""Example 52: DynamoDB GSI Access Pattern."""  # => co-23,co-17: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => co-17: boto3's dynamic resource/client factory has no stubs pinned -- Any is the honest, explicit type

import boto3  # => co-17: the official AWS SDK for Python
from boto3.dynamodb.conditions import Key  # => co-17: a typed helper for building KeyConditionExpressions safely


def get_local_dynamodb_resource() -> Any:  # => co-17: the higher-level "resource" API
    """Return a boto3 DynamoDB resource pointed at a local dynamodb-local instance."""  # => documents the contract
    return boto3.resource(  # => co-17: same endpoint/credential pattern as prior DynamoDB examples
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="us-east-1",  # => the local dynamodb-local endpoint, no real AWS account needed
        aws_access_key_id="fake",
        aws_secret_access_key="fake",  # => dynamodb-local accepts any credentials
    )  # => closes the boto3.resource() call -- returns a high-level resource bound to the local endpoint


def create_table_with_gsi(resource: Any) -> None:  # => co-17,co-23: base table keyed one way, GSI re-keys the SAME items a second way
    """Create a table keyed by order_id, with a GSI re-projecting the same items keyed by customer_id."""  # => documents contract
    client = resource.meta.client  # => the underlying low-level client, needed for list/delete/waiter calls
    if "OrdersWithGsi" in client.list_tables()["TableNames"]:  # => resets state -- this example is fully self-contained
        client.delete_table(TableName="OrdersWithGsi")  # => removes any leftover table from a prior run
        client.get_waiter("table_not_exists").wait(TableName="OrdersWithGsi")  # => blocks until the delete genuinely completes
    resource.create_table(  # => co-23: the BASE table's own key answers "fetch one order by order_id" -- and nothing else
        TableName="OrdersWithGsi",  # => the table this whole GSI example uses
        KeySchema=[{"AttributeName": "order_id", "KeyType": "HASH"}],  # => co-23: the base table's ONLY access pattern
        AttributeDefinitions=[  # => declares every attribute used by EITHER the base table key OR the GSI key
            {"AttributeName": "order_id", "AttributeType": "S"},  # => the base table's own partition key attribute
            {"AttributeName": "customer_id", "AttributeType": "S"},  # => co-17: needed because the GSI below partitions by it
        ],  # => closes the AttributeDefinitions list -- both attributes declared, base-key and GSI-key alike
        GlobalSecondaryIndexes=[  # => co-17,co-23: a SECOND access pattern the base table's own key cannot serve
            {  # => the GSI definition dict starts here
                "IndexName": "customer_id-index",  # => co-17: a named, independently queryable index
                "KeySchema": [{"AttributeName": "customer_id", "KeyType": "HASH"}],  # => co-17: re-partitions the SAME items by customer_id
                "Projection": {"ProjectionType": "ALL"},  # => co-17: copies every attribute into the index, no extra base-table fetch needed
                "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => the GSI's OWN, separately provisioned throughput
            }  # => closes this one GSI's own definition dict
        ],  # => closes the GlobalSecondaryIndexes list -- exactly one GSI defined here
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => local-testing throughput for the base table
    )  # => closes the create_table() call -- both the base table AND its GSI now exist
    client.get_waiter("table_exists").wait(TableName="OrdersWithGsi")  # => blocks until BOTH the table and the GSI are genuinely ready


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    resource = get_local_dynamodb_resource()  # => connects to the local dynamodb-local Docker container
    create_table_with_gsi(resource)  # => sets up the fresh table + GSI
    table = resource.Table("OrdersWithGsi")  # => the high-level Table object the resource API works through

    table.put_item(Item={"order_id": "o-1", "customer_id": "cust-9", "amount": 20})  # => co-23: 2 of these 3 orders share customer_id=cust-9
    table.put_item(Item={"order_id": "o-2", "customer_id": "cust-9", "amount": 35})  # => co-23: same customer, DIFFERENT order_id partition key
    table.put_item(Item={"order_id": "o-3", "customer_id": "cust-1", "amount": 15})  # => a different customer entirely

    # The BASE table's key (order_id) CANNOT answer "all orders for cust-9" -- that needs a full scan without the GSI.
    gsi_response = table.query(  # => co-17: querying the GSI, NOT the base table's own primary key
        IndexName="customer_id-index",  # => co-17: routes this query through the secondary index specifically
        KeyConditionExpression=Key("customer_id").eq("cust-9"),  # => co-17: an access pattern the base table's own key alone could never serve
    )  # => closes the query() call -- only the customer_id-index gets scanned, never the full base table
    items = gsi_response["Items"]  # => the orders the GSI found for this customer
    order_ids = sorted(item["order_id"] for item in items)  # => extracts order_ids for a deterministic assertion
    assert order_ids == ["o-1", "o-2"]  # => co-23,co-17: BOTH of cust-9's orders found, via a query the base table key structure alone couldn't answer
    print(f"GSI query for customer_id=cust-9 (base table key alone could not answer this): {order_ids}")  # => Output: GSI query for customer_id=cust-9 (base table key alone could not answer this): ['o-1', 'o-2']


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
