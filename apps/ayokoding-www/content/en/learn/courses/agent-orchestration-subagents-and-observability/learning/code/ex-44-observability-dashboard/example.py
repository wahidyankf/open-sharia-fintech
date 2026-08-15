# A dashboard joins the three key operational signal types.
dashboard = {"trace": "run", "metrics": "cost", "eval": "pass"}
# All signals refer to the same local run.
assert set(dashboard) == {"trace", "metrics", "eval"}
# Print the compact dashboard.
print(dashboard)
