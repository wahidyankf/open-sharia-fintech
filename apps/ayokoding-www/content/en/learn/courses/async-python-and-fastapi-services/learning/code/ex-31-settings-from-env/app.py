"""Example 31: Loading Config from Env with pydantic settings.

pydantic-settings loads typed config from environment variables, so an env override applies and a missing
required value fails fast at startup. Run: APP_PORT=9000 uvicorn app:app --port 8000, then:
curl localhost:8000/config  (co-24)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic_settings import BaseSettings, SettingsConfigDict  # => typed settings from env (co-24)

app = FastAPI()  # => the ASGI application uvicorn serves


class Settings(BaseSettings):  # => each field is read from a matching env var at construction (co-24)
    model_config = SettingsConfigDict(env_prefix="APP_")  # => APP_ prefix: field "port" <- env "APP_PORT"

    env: str = "dev"  # => defaults when the env var is absent
    port: int = 8000  # => a typed int -- a non-integer env value fails fast at startup (co-24)


settings = Settings()  # => constructed ONCE; an env override (APP_PORT=9000) lands here (co-24)


@app.get("/config")  # => a route exposing the resolved config
def read_config() -> dict[str, object]:  # => the settings as JSON
    return {"env": settings.env, "port": settings.port}  # => reflects any env override (co-24, co-14)
