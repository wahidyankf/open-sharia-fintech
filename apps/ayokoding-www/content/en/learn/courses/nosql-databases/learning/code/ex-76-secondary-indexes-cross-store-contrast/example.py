"""Example 76: Secondary Indexes, Cross-Store Contrast."""  # => co-17: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => co-17: gives the new index a moment to finish its asynchronous build before querying it
from typing import Any  # => co-17: boto3's dynamic resource/client factory has no stubs pinned -- Any is the honest, explicit type

import boto3  # => co-17: the official AWS SDK for Python
from boto3.dynamodb.conditions import Key  # => co-17: a typed helper for building KeyConditionExpressions safely
from cassandra.cluster import Cluster, Session  # => co-17: cassandra-driver, the Apache Software Foundation-maintained Python driver
from pymongo import MongoClient  # => co-17: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-17: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document

# The SAME shaped query, asked of all 3 stores: "find every order placed by customer_id=cust-1"


def mongo_secondary_index_query(client: MongoClient[Document]) -> list[int]:  # => co-17: MongoDB's secondary index -- SAME collection, ADDITIONAL index
    """Seed orders in MongoDB, add a secondary index on customer_id, and query by it."""  # => documents the contract
    collection = client["nosqldb"]["orders_76"]  # => a dedicated collection for this contrast
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many([{"customer_id": "cust-1", "amount": i * 10} for i in range(3)])  # => co-17: 3 matching orders
    collection.insert_many([{"customer_id": "cust-2", "amount": 999}])  # => a non-matching order, to prove the filter genuinely works
    collection.create_index("customer_id")  # => co-17: a secondary index -- lives WITHIN the SAME collection, alongside the documents
    matched = list(collection.find({"customer_id": "cust-1"}))  # => co-17: the index-served query
    return sorted(doc["amount"] for doc in matched)  # => hand back the amounts, sorted for a deterministic assertion


def cassandra_secondary_index_query(session: Session) -> list[int]:  # => co-17: Cassandra's secondary index -- requires a cross-node fan-out (Example 59)
    """Seed orders in Cassandra, add a secondary index on customer_id, and query by it."""  # => documents the contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS orders_76")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: order_id is the PARTITION key -- customer_id is NOT part of the key at all
        "CREATE TABLE orders_76 (order_id int PRIMARY KEY, customer_id text, amount int)"  # => closes the CREATE TABLE statement -- customer_id is a plain, non-key column
    )  # => closes the execute() call -- the table now exists with this exact key layout
    for i in range(3):  # => co-17: 3 matching orders, EACH in its OWN partition (order_id is the key)
        session.execute("INSERT INTO orders_76 (order_id, customer_id, amount) VALUES (%s, %s, %s)", (i, "cust-1", i * 10))  # => positional CQL placeholders bind the loop's own values
    session.execute("INSERT INTO orders_76 (order_id, customer_id, amount) VALUES (%s, %s, %s)", (99, "cust-2", 999))  # => a non-matching order
    session.execute("CREATE INDEX IF NOT EXISTS ON orders_76 (customer_id)")  # => co-17: a secondary index -- built PER NODE, queried via cluster-wide fan-out
    time.sleep(3)  # => co-17: same asynchronous-build wait Example 59 required
    matched = list(session.execute("SELECT amount FROM orders_76 WHERE customer_id = %s", ("cust-1",)))  # => co-17: the FAN-OUT, index-served query
    return sorted(row.amount for row in matched)  # => hand back the amounts, sorted for a deterministic assertion


def dynamodb_gsi_query() -> list[int]:  # => co-17: DynamoDB's GSI -- a SEPARATE, independently-keyed and -provisioned index
    """Seed orders in DynamoDB, add a GSI on customer_id, and query it via boto3."""  # => documents the contract
    resource: Any = boto3.resource(  # => connects to the local dynamodb-local Docker container
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="us-east-1",  # => the local dynamodb-local endpoint, no real AWS account needed
        aws_access_key_id="fake",
        aws_secret_access_key="fake",  # => dynamodb-local accepts any credentials
    )  # => closes the boto3.resource() call -- returns a high-level resource bound to the local endpoint
    client = resource.meta.client  # => the underlying low-level client, needed for list/delete/waiter calls
    if "Orders76" in client.list_tables()["TableNames"]:  # => resets state -- this example is fully self-contained
        client.delete_table(TableName="Orders76")  # => removes any leftover table from a prior run
        client.get_waiter("table_not_exists").wait(TableName="Orders76")  # => blocks until the delete genuinely completes
    resource.create_table(  # => co-23: order_id is the BASE table's own key -- customer_id needs a SEPARATE GSI
        TableName="Orders76",  # => the table this whole cross-store contrast example uses
        KeySchema=[{"AttributeName": "order_id", "KeyType": "HASH"}],  # => co-23: the base table's ONLY access pattern
        AttributeDefinitions=[{"AttributeName": "order_id", "AttributeType": "S"}, {"AttributeName": "customer_id", "AttributeType": "S"}],  # => declares both the base key AND the GSI key attributes
        GlobalSecondaryIndexes=[
            {  # => co-17: a NAMED, independently PROVISIONED index -- distinct from Cassandra's per-node build
                "IndexName": "customer_id-index",  # => a named, independently queryable index
                "KeySchema": [{"AttributeName": "customer_id", "KeyType": "HASH"}],  # => re-partitions the SAME items by customer_id
                "Projection": {"ProjectionType": "ALL"},  # => copies every attribute into the index, no extra base-table fetch needed
                "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => the GSI's OWN, separately provisioned throughput
            }
        ],  # => closes this one GSI's own definition dict
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},  # => local-testing throughput for the base table
    )  # => closes the create_table() call -- both the base table AND its GSI now exist
    client.get_waiter("table_exists").wait(TableName="Orders76")  # => blocks until BOTH the table and the GSI are genuinely ready
    table = resource.Table("Orders76")  # => the high-level Table object the resource API works through
    for i in range(3):  # => co-17: 3 matching orders, each with its own order_id partition key
        table.put_item(Item={"order_id": f"o-{i}", "customer_id": "cust-1", "amount": i * 10})  # => co-17: every matching order re-uses cust-1, the shared filter value
    table.put_item(Item={"order_id": "o-99", "customer_id": "cust-2", "amount": 999})  # => a non-matching order
    response = table.query(IndexName="customer_id-index", KeyConditionExpression=Key("customer_id").eq("cust-1"))  # => co-17: the GSI-served query
    return sorted(int(item["amount"]) for item in response["Items"])  # => hand back the amounts, sorted for a deterministic assertion


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    mongo_client: MongoClient[Document] = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    cassandra_cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    cassandra_session = cassandra_cluster.connect()  # => opens a session against that cluster

    mongo_result = mongo_secondary_index_query(mongo_client)  # => co-17: MongoDB's own answer to the shared query
    cassandra_result = cassandra_secondary_index_query(cassandra_session)  # => co-17: Cassandra's own answer to the shared query
    dynamo_result = dynamodb_gsi_query()  # => co-17: DynamoDB's own answer to the shared query

    expected = [0, 10, 20]  # => co-17: the SAME shared expectation for all 3 stores, since they seed the identical logical data
    assert mongo_result == cassandra_result == dynamo_result == expected  # => co-17: EVERY store returns the IDENTICAL result set for the SAME shaped query
    print(f"MongoDB secondary index:    {mongo_result}")  # => Output: MongoDB secondary index:    [0, 10, 20]
    print(f"Cassandra secondary index:  {cassandra_result}")  # => Output: Cassandra secondary index:  [0, 10, 20]
    print(f"DynamoDB GSI:                {dynamo_result}")  # => Output: DynamoDB GSI:                [0, 10, 20]
    print("Identical results, 3 different index architectures: Mongo=in-collection index, Cassandra=per-node index+fan-out, DynamoDB=separately provisioned GSI")  # => Output line

    mongo_client.close()  # => always release what you open
    cassandra_cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
