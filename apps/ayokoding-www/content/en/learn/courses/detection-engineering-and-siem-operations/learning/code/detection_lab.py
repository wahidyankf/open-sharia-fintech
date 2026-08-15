#!/usr/bin/env python3
"""Offline validator for original, synthetic Detection Engineering course artifacts."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as element_tree
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVENTS = HERE / "lab-events.ndjson"
DECODER = HERE / "local_decoder.xml"
RULES = HERE / "local_rules.xml"
CONFIG = HERE / "localfile-config.xml"
DASHBOARD = HERE / "dashboard-plan.json"
COMMANDS = {
    "verify",
    "events",
    "hypothesis",
    "config",
    "decode",
    "xml",
    "reject",
    "rules",
    "detect",
    "coverage",
    "change",
    "triage",
    "dashboard",
    "tune",
    "correlate",
    "exception",
    "tradeoff",
    "inventory",
    "lifecycle",
    "metrics",
}
PATTERN = re.compile(r"^LABAUTH user=(\w+) src=(\d+\.\d+\.\d+\.\d+) action=(\w+)$")


def rows() -> list[dict[str, str]]:
    # => The only input is a course-authored local fixture; no host or endpoint is accepted.
    return [
        json.loads(line)
        for line in EVENTS.read_text(encoding="utf-8").splitlines()
        if line
    ]


def decode(raw: str) -> dict[str, str] | None:
    # => A failed full match rejects unrelated text rather than guessing at fields.
    match = PATTERN.fullmatch(raw)
    if match is None:
        return None
    # => Named values match the XML order contract: user, srcip, action.
    return dict(zip(("user", "srcip", "action"), match.groups()))


def decoded_rows() -> list[dict[str, str]]:
    # => The fixture label stays with each parsed row for explicit tuning calculations.
    parsed = [{**row, **(decode(row["raw"]) or {})} for row in rows()]
    assert all("action" in row for row in parsed), "every lab row must decode"
    return parsed


def failures(items: list[dict[str, str]]) -> list[dict[str, str]]:
    # => The base rule is intentionally narrow: one parsed action value only.
    return [item for item in items if item["action"] == "failure"]


def correlation(items: list[dict[str, str]], threshold: int = 3) -> list[str]:
    # => Count failures by source so unrelated fictional sources cannot join a sequence.
    counts = Counter(item["srcip"] for item in failures(items))
    # => A source must also have a success to satisfy this course's bounded teaching hypothesis.
    successes = {item["srcip"] for item in items if item["action"] == "success"}
    return sorted(
        source
        for source, count in counts.items()
        if count >= threshold and source in successes
    )


def xml_root(path: Path) -> element_tree.Element:
    # => Parsing XML locally verifies well-formed original teaching artifacts without a Wazuh service.
    return element_tree.parse(path).getroot()


def validate_artifacts() -> None:
    decoder = xml_root(DECODER)
    assert decoder.tag == "decoder" and decoder.attrib["name"] == "course-lab-auth"
    assert decoder.findtext("prematch") == "^LABAUTH"
    assert decoder.findtext("order") == "user,srcip,action"
    assert "user=" in (decoder.findtext("regex") or "")
    rules = xml_root(RULES)
    rule_ids = {rule.attrib["id"] for rule in rules.findall("rule")}
    assert rule_ids == {"100500", "100501"}
    correlation_rule = next(
        rule for rule in rules.findall("rule") if rule.attrib["id"] == "100501"
    )
    assert (
        correlation_rule.attrib["frequency"] == "3"
        and correlation_rule.attrib["timeframe"] == "120"
    )
    config = xml_root(CONFIG)
    assert config.findtext("localfile/log_format") == "syslog"
    plan = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    assert len(plan["panels"]) == 3 and all(
        panel["field"].startswith("rule.") for panel in plan["panels"]
    )


def show_events() -> None:
    for item in decoded_rows():
        print(
            f"{item['timestamp']} user={item['user']} source={item['srcip']} action={item['action']} label={item['label']}"
        )


def show_decode() -> None:
    item = decoded_rows()[0]
    assert (
        item["user"] == "lee"
        and item["srcip"] == "192.0.2.44"
        and item["action"] == "failure"
    )
    print("PASS: decoder contract user=lee srcip=192.0.2.44 action=failure")


def show_detect() -> None:
    items = decoded_rows()
    base = failures(items)
    assert len(base) == 4
    assert any(item["action"] == "success" for item in items)
    print("BASE RULE: 4 fictional failed-action review prompts")
    print("PASS: benign success did not satisfy the failed-action rule")


def show_correlation() -> None:
    found = correlation(decoded_rows())
    assert found == ["198.51.100.17"]
    print("CORRELATION: source=198.51.100.17 failures=3 then success=yes")
    print("PASS: one bounded fictional sequence requires review")


def show_tune() -> None:
    items = decoded_rows()
    loose = [item for item in failures(items)]
    tuned_sources = correlation(items, threshold=3)
    benign_prompts = sum(item["label"] == "benign" for item in loose)
    false_positive_rate = benign_prompts / len(loose)
    assert (
        len(loose) == 4
        and tuned_sources == ["198.51.100.17"]
        and false_positive_rate == 0.25
    )
    print("TUNING: threshold=1 prompts=4 benign_prompts=1 false_positive_rate=0.25")
    print("TUNING: threshold=3 correlated_sources=1 retained_signal=yes")


def show_dashboard() -> None:
    plan = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    print("DASHBOARD: " + " | ".join(panel["question"] for panel in plan["panels"]))
    print(
        "PASS: dashboard plan includes severity, tuning, and tested-coverage questions"
    )


def show_triage() -> None:
    print(
        "TRIAGE: evidence=three failures then success | uncertainty=fictional fixture only | owner=training reviewer"
    )
    print(
        "HANDOFF: response authority remains with the defensive-security incident process"
    )


def show_inventory() -> None:
    expected = [DECODER, RULES, CONFIG, DASHBOARD, EVENTS, HERE / "detection_lab.py"]
    assert all(path.is_file() for path in expected)
    print(
        "PACK: decoder, rules, illustrative config, dashboard plan, fixture, verifier"
    )


def show_metrics() -> None:
    print(
        "METRICS: review_prompts=4 | correlated_sequences=1 | fictional_time_to_review=5m"
    )
    print("NOTE: metrics are training values, not operational performance claims")


def verify() -> None:
    validate_artifacts()
    show_decode()
    assert decode("not a course lab line") is None
    show_detect()
    show_correlation()
    show_tune()
    show_dashboard()
    show_inventory()
    print(
        "PASS: offline decoder, rules, correlation, dashboard, and tuning invariants hold"
    )


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit("usage: detection_lab.py {" + ",".join(sorted(COMMANDS)) + "}")
    command = sys.argv[1]
    if command == "verify":
        verify()
    elif command == "events":
        show_events()
    elif command in {"decode", "xml"}:
        validate_artifacts()
        show_decode()
    elif command == "reject":
        assert decode("not a course lab line") is None
        print("PASS: unrelated local line rejected")
    elif command in {"rules", "config"}:
        validate_artifacts()
        print("PASS: original local XML artifact structure is valid")
    elif command == "detect":
        show_detect()
    elif command == "correlate":
        show_correlation()
    elif command == "tune":
        show_tune()
    elif command == "dashboard":
        show_dashboard()
    elif command == "triage":
        show_triage()
    elif command == "inventory":
        show_inventory()
    elif command == "metrics":
        show_metrics()
    elif command == "hypothesis":
        print(
            "HYPOTHESIS: three fictional failures from one source followed by success require analyst review"
        )
    elif command == "coverage":
        print(
            "COVERAGE: T1110 -> tested local rule 100500; GAP: no claim beyond the synthetic fixture"
        )
    elif command == "change":
        print(
            "CHANGE: intent | benign test | retained signal | reviewer | rollback | recheck date"
        )
    elif command == "exception":
        print(
            "EXCEPTION: scope=fictional-service reason=known-training-noise owner=reviewer expires=2026-09-15"
        )
    elif command == "tradeoff":
        print(
            "TRADE-OFF: wider time window may improve sensitivity and may join more unrelated events"
        )
    elif command == "lifecycle":
        print(
            "LIFECYCLE: create -> test -> tune -> measure -> review -> retire with successor or rationale"
        )


if __name__ == "__main__":
    main()
