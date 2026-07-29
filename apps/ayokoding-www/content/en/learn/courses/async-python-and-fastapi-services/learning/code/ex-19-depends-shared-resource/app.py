"""Example 19: Injecting a Shared Resource with Depends.

Run: uvicorn app:app --port 8000, then: curl localhost:8000/config  (co-15)
"""

from fastapi import Depends, FastAPI  # => Depends is FastAPI's dependency-injection verb (co-15)

app = FastAPI()  # => the ASGI application uvicorn serves


class AppConfig:  # => a shared resource every handler can declare as a dependency
    def __init__(self, env: str = "dev") -> None:  # => a value the whole app shares
        self.env = env  # => the active environment name


def get_config() -> AppConfig:  # => a DEPENDENCY PROVIDER -- a plain callable Depends resolves per request
    return AppConfig(env="dev")  # => a shared instance handed to every handler that declares it (co-15)


@app.get("/config")  # => a route that NEEDS the shared config
def read_config(config: AppConfig = Depends(get_config)) -> dict[str, str]:  # => Depends wires the provider in
    # => the handler never calls get_config itself -- the framework does, then passes the result in (co-15)
    return {"env": config.env}  # => the injected resource's value, as JSON (co-14)
