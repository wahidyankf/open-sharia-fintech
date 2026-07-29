# pyright: strict
"""Example 49: Health check -- /livez (liveness). (co-27)

A liveness probe reports whether the process itself is healthy. A liveness
FAILURE causes the orchestrator (e.g. kubelet) to RESTART the container.
This example reports healthy normally, then unhealthy when an internal
liveness flag trips. Source: Kubernetes probes docs.
"""

from dataclasses import dataclass  # => a small typed response record


@dataclass  # => co-27: status + a short message
class Response:
    status: int  # => 200 healthy, 503 unhealthy
    body: dict[str, str]  # => a short status message


class Liveness:  # => co-27: the process's own internal liveness flag
    def __init__(self) -> None:
        self.alive = True  # => healthy until something fatal trips it

    def crash(self) -> None:  # => simulate a fatal internal condition
        self.alive = False  # => co-27: a liveness failure -> kubelet would RESTART


def livez(probe: Liveness) -> Response:  # => GET /livez
    if probe.alive:  # => co-27: process is alive
        return Response(200, {"status": "ok"})  # => 200 -- no restart needed
    return Response(503, {"status": "unhealthy"})  # => co-27: 503 -> triggers a container RESTART


probe = Liveness()  # => co-27: starts healthy
healthy = livez(probe)  # => alive -> 200
print(f"healthy: status={healthy.status}, body={healthy.body}")  # => Output: 200

probe.crash()  # => co-27: simulate a fatal condition
unhealthy = livez(probe)  # => not alive -> 503 (triggers restart)
print(f"after crash: status={unhealthy.status}, body={unhealthy.body}")  # => Output: 503

assert healthy.status == 200 and unhealthy.status == 503  # => co-27: liveness reports healthy then unhealthy
