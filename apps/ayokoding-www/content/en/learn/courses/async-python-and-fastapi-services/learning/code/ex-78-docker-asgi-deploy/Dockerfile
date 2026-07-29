# Example 78: A Dockerfile for Multi-Worker ASGI Deploy
# syntax=docker/dockerfile:1
# => a slim, reproducible production image running uvicorn with N workers behind the ASGI app (co-24)

# => build stage uses the pinned python base -- reproducible, slim
FROM python:3.13-slim AS base

# => set working directory inside the image
WORKDIR /app

# => install the exact runtime pins (co-07) -- uvicorn[standard] adds uvloop/httptools for production speed
RUN pip install --no-cache-dir \
      "fastapi==0.139.0" \
      "uvicorn[standard]==0.51.0" \
      "pydantic==2.11.0" \
      "aiosqlite==0.20.0"

# => copy the application code into the image
COPY main.py .

# => expose the port uvicorn listens on
EXPOSE 8000

# => run uvicorn with MULTIPLE workers -- one process per core, behind one port (co-24)
# => --workers 4 runs 4 ASGI processes; each owns its own event loop (co-02, co-24)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
