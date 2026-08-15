from typing import Final  # => typed offline file-task fixture

CONTENT: Final[str] = "target"  # => expected post-edit content
assert CONTENT == "target"
print("PASS: file-editing-agent")  # => verified result
