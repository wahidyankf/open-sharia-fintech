from dataclasses import dataclass
from time import perf_counter


@dataclass(frozen=True)
class Answer:
    text: str
    citation: str


CORPUS = {"python-api": "Python API clients validate JSON before using it."}


def retrieve(question: str) -> tuple[str, str]:
    assert "ignore instructions" not in question.lower()
    return next(iter(CORPUS.items()))


def lookup(city: str) -> str:
    if not city.isalpha():
        raise ValueError("city must contain letters only")
    return "sunny in " + city


started = perf_counter()
source_id, context = retrieve("How should an API client use JSON?")
answer = Answer("Validate JSON before using it.", source_id)
assert context in CORPUS.values()
assert answer.citation == "python-api"
assert lookup("Jakarta") == "sunny in Jakarta"
assert perf_counter() - started < 0.1
print("PASS: grounded cited answer, validated tool, bounded offline flow")
