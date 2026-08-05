"""Define a container image that packages the CLI."""

dockerfile = """FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install .
ENTRYPOINT ["notes-linux"]
"""
print(dockerfile)
