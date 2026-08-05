"""Show a container run command with a mounted Unix-socket directory."""

image = "notes-linux:dev"
command = f"docker run --rm -v /tmp:/tmp {image} status --socket /tmp/notes-linux.sock"
print(command)
