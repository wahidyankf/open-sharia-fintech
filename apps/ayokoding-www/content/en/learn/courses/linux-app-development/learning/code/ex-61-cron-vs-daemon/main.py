"""Choose cron for scheduled work and a daemon for continuous work."""

workloads = {"daily cleanup": "cron", "socket status API": "daemon"}
for workload, runner in workloads.items():
    print(f"{workload}: {runner}")
