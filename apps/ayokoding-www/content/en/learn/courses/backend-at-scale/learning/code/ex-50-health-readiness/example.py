# pyright: strict
"""Example 50: Health check -- /readyz (readiness). (co-27)

A readiness probe reports whether the pod is ready to receive traffic. A
readiness FAILURE removes the pod from the Service's endpoints (it stops
getting requests) but does NOT restart it -- distinct from liveness. This
example shows unready while a dependency (DB) is down. Source: Kubernetes
probes docs.
"""

from dataclasses import dataclass  # => a small typed response record


@dataclass  # => co-27: status + a short message
class Response:
    status: int  # => 200 ready, 503 unready
    body: dict[str, str]  # => a short status message


class Readiness:  # => co-27: tracks whether dependencies are available
    def __init__(self) -> None:
        self.db_up = True  # => the dependency's availability

    def db_goes_down(self) -> None:  # => simulate a dependency outage
        self.db_up = False  # => co-27: dependency down -> unready (but NOT a restart)

    def db_recovers(self) -> None:  # => simulate the dependency recovering
        self.db_up = True  # => ready again


def readyz(probe: Readiness) -> Response:  # => GET /readyz
    if not probe.db_up:  # => co-27: dependency down -> unready
        return Response(503, {"status": "unready", "reason": "db down"})  # => 503 -> removed from endpoints, NOT restarted
    return Response(200, {"status": "ready"})  # => 200 -> receives traffic


probe = Readiness()  # => co-27: starts ready (dependency up)
ready = readyz(probe)  # => db up -> 200
print(f"ready: status={ready.status}, body={ready.body}")  # => Output: 200

probe.db_goes_down()  # => co-27: dependency outage -> unready (not restarted)
unready = readyz(probe)  # => db down -> 503
print(f"db down: status={unready.status}, body={unready.body}")  # => Output: 503, removed from endpoints

probe.db_recovers()  # => dependency recovers -> ready again (no restart was needed)
recovered = readyz(probe)  # => db up -> 200
print(f"recovered: status={recovered.status}, body={recovered.body}")  # => Output: 200

assert ready.status == 200 and unready.status == 503 and recovered.status == 200  # => co-27: readiness tracks the dependency
