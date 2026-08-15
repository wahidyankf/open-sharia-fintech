# A post-hook receives the completed result.
def after(result: str) -> str:
    # The extension adds metadata without changing the tool.
    return f"{result}:observed"


# The local tool result crosses the post-call seam.
observed = after("ok")
# The output proves post-processing ran.
assert observed == "ok:observed"
# Print the observed result.
print(observed)
