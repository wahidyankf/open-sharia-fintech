# pyright: strict
"""Example 71: Broker backplane -- fanout across two app nodes. (co-34)

WebSocket/SSE connections are STICKY to the one node that accepted them.
Broadcasting an event to clients connected to DIFFERENT nodes requires a
shared pub/sub BACKPLANE: a node publishes once, the backplane fans the
message out to every node, and each node delivers to its own sticky clients.
Source: Socket.IO Redis adapter (relies on Redis Pub/Sub).
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-34: one app node holding its own sticky client connections
class AppNode:
    name: str  # => the node's label
    clients: list[str] = field(default_factory=list[str])  # => sticky clients connected to THIS node
    delivered: list[str] = field(default_factory=list[str])  # => messages this node delivered locally

    def deliver(self, message: str) -> list[str]:  # => push a message to THIS node's own sticky clients
        recipients = list(self.clients)  # => the local clients
        self.delivered.append(message)  # => record local delivery
        return recipients  # => who got it on this node


@dataclass  # => co-34: the shared pub/sub backplane that fans messages across nodes
class Backplane:
    nodes: list[AppNode] = field(default_factory=list[AppNode])  # => every node subscribed to the backplane

    def register(self, node: AppNode) -> None:  # => a node joins the backplane
        self.nodes.append(node)  # => subscribed

    def broadcast(self, message: str) -> dict[str, list[str]]:  # => co-34: publish once -> fan out to every node
        reached: dict[str, list[str]] = {}  # => node -> its local recipients
        for node in self.nodes:  # => every node gets the message via the backplane
            reached[node.name] = node.deliver(message)  # => each node delivers to its OWN sticky clients
        return reached  # => who received the message, per node


backplane = Backplane()  # => co-34: the shared pub/sub backplane
node_a = AppNode("A", clients=["client-1", "client-2"])  # => node A holds 2 sticky clients
node_b = AppNode("B", clients=["client-3"])  # => node B holds 1 sticky client
backplane.register(node_a)  # => A joins the backplane
backplane.register(node_b)  # => B joins the backplane

reached = backplane.broadcast("hello")  # => co-34: one broadcast -> clients on BOTH nodes receive it
print(f"broadcast reached: {reached}")  # => Output: A->[client-1,client-2], B->[client-3]

all_clients = reached["A"] + reached["B"]  # => every client across both nodes
print(f"all clients that received 'hello': {all_clients}")  # => Output: all 3 clients

assert all_clients == ["client-1", "client-2", "client-3"]  # => co-34: the backplane fanned out to both nodes
