# Example 28: Dockerfile Deploy on the PaaS. (co-17)
#
# The "control" half of co-17's trade-off: instead of a buildpack detecting
# your language, YOU specify the exact image, layer by layer. The PaaS detects
# this Dockerfile and builds from IT (ignoring the Procfile from Example 27).
# Deploy with the same `git push` (Example 26) -- only the build recipe changes.

# pin the frontend parser for reproducible builds
# syntax=docker/dockerfile:1
# specific tag (not 'latest'); slim base keeps the image small
FROM docker.io/library/python:3.12-slim

# hadolint wants apt-get piped through no-install-recommends and a cleanup in one layer:
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# every subsequent path (COPY, RUN) resolves here
WORKDIR /app

# Copy the dependency manifest FIRST and install once -> this layer is cached
# across rebuilds as long as requirements.txt does not change.
# manifest alone, so dependency install caches independently of code
COPY requirements.txt ./
# --no-cache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code (changes every push -> invalidates only this thin layer).
# the same service reused from backend-essentials / Example 6
COPY app.py ./

# Run as a NON-ROOT user (co-04 discipline, inside the container too).
# a dedicated unprivileged user
RUN useradd --create-home appuser
# all subsequent commands (and the final CMD) run as appuser, not root
USER appuser

# The PaaS injects $PORT and routes its proxy to this port inside the container.
# default; the PaaS overrides it at runtime
ENV PORT=5000
# DOCUMENTS the port (the PaaS maps it; this does not publish it)
EXPOSE 5000

# gunicorn serves the app (matches the Procfile's web command from Example 27).
# exec form (JSON array), the preferred form
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

# --- Verify (after `git push`) ------------------------------------------------
#   ssh dokku@<box> ps:report myapp   # => 'Dockerfile build' (not 'buildpack')
#   curl http://<box>/<app-url>       # => parity with Example 27's buildpack build
# [verify] the Dockerfile and buildpack deploys serve the SAME app (co-17 parity).
