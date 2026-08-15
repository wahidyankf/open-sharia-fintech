#!/usr/bin/env python3
"""Safe offline blue-team lab over original synthetic telemetry."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVENTS = HERE / "lab-events.ndjson"
ALLOWED = {
    "verify",
    "detect",
    "bulk",
    "hunt",
    "timeline",
    "ir",
    "hardening",
    "coverage",
    "tabletop",
    "roles",
}


def events() -> list[dict[str, str]]:
    # => Keeping events in a local fixture prevents accidental collection of live telemetry.
    return [
        json.loads(line)
        for line in EVENTS.read_text(encoding="utf-8").splitlines()
        if line
    ]


def detections(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    # => Count failed authentication attempts by source so the threshold is explicit and reviewable.
    failures = Counter(
        row["source_ip"] for row in rows if row["event_type"] == "auth_failure"
    )
    found = [
        {
            "rule": "failed-login-burst",
            "source": source,
            "attack": "T1110",
            "count": str(count),
        }
        for source, count in failures.items()
        if count
        >= 3  # => A threshold of three leaves the fixture's single benign typo quiet.
    ]
    for row in rows:
        # => The invented marker represents parser rejection, not an exploit payload.
        if row["event_type"] == "web_request" and row["outcome"] == "parser_rejected":
            found.append(
                {
                    "rule": "suspicious-request-evidence",
                    "source": row["source_ip"],
                    "attack": "T1190",
                    "count": "1",
                }
            )
    return found


def detect() -> None:
    found = detections(events())
    assert len(found) == 2, (
        "the original fixture must yield exactly two reviewable alerts"
    )
    for alert in found:
        print(
            f"ALERT {alert['rule']} source={alert['source']} ATT&CK={alert['attack']} count={alert['count']}"
        )
    print("PASS: benign single failure stayed below the threshold")


def bulk() -> None:
    # => Printing action/source pairs permits review before an owner imports into a local OpenSearch lab.
    for row in events():
        print(json.dumps({"index": {"_index": "blue-lab-events"}}, sort_keys=True))
        print(json.dumps(row, sort_keys=True))
    print("PASS: generated offline OpenSearch bulk NDJSON", file=sys.stderr)


def hunt() -> None:
    rows = [row for row in events() if row["source_ip"] == "192.0.2.44"]
    assert len(rows) == 4, "the fixture intentionally has four related events"
    print("HUNT: repeated authentication failure plus parser-rejected request evidence")
    for row in rows:
        print(f"{row['timestamp']} {row['event_type']} {row['outcome']}")
    print("PASS: local pivot joined four events without contacting any host")


def timeline() -> None:
    for row in events():
        print(
            f"{row['timestamp']} | {row['source_ip']} | {row['event_type']} | {row['outcome']}"
        )
    print("PASS: timeline derives from normalized local fields")


def ir() -> None:
    print(
        "IR tabletop: prepare -> detect-analyze -> contain -> eradicate -> recover -> lessons-learned"
    )
    print(
        "Current note: NIST SP 800-61 Rev. 3 maps IR considerations to CSF 2.0 functions."
    )
    print("PASS: record decision, owner, evidence reference, and recovery check")


def hardening() -> None:
    baseline = {
        "admin_remote_login": True,
        "unused_demo_service": True,
        "segment_default": "allow",
    }
    desired = {
        "admin_remote_login": False,
        "unused_demo_service": False,
        "segment_default": "deny",
    }
    for key in baseline:
        print(f"{key}: {baseline[key]} -> {desired[key]}")
    print("PASS: hardening reduces exposure before an alert must fire")


def coverage() -> None:
    for technique, rule in {
        "T1110": "failed-login-burst",
        "T1190": "suspicious-request-evidence",
    }.items():
        print(f"{technique}: {rule}")
    print(
        "GAP RULE: each authorized lab finding needs detection plus remediation before closure"
    )


def roles() -> None:
    print(
        "BLUE: detect, contain, recover | RED: validate an authorized lab | PURPLE: turn finding into coverage"
    )
    print("PASS: this course stays on the defensive side of the loop")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ALLOWED:
        raise SystemExit("usage: blue_lab.py {" + ",".join(sorted(ALLOWED)) + "}")
    command = sys.argv[1]
    actions = {
        "detect": detect,
        "bulk": bulk,
        "hunt": hunt,
        "timeline": timeline,
        "ir": ir,
        "hardening": hardening,
        "coverage": coverage,
        "tabletop": ir,
        "roles": roles,
    }
    if command == "verify":
        # => Verification proves fixture, detection, hunt, response, and hardening work together.
        detect()
        hunt()
        ir()
        hardening()
        coverage()
        return
    actions[command]()


if __name__ == "__main__":
    main()
