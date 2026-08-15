# Pathlib resolves a path before authority is granted.
from pathlib import Path

# The sandbox root is the sole authorized filesystem region.
ROOT = Path("/sandbox").resolve()


# Validation rejects paths that do not remain below ROOT.
def allowed(path: str) -> bool:
    # Relative resolution makes traversal attempts visible.
    return str(Path(path).resolve()).startswith(str(ROOT) + "/")


# A parent traversal must not receive file-tool authority.
assert not allowed("/sandbox/../secret")
# Print the rejected traversal decision.
print(allowed("/sandbox/../secret"))
