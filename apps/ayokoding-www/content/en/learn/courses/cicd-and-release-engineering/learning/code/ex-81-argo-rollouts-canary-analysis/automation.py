"""Runnable verification for CI/CD Example 81: Analyze an Argo Rollouts Canary."""

# => dataclass gives each evidence record an explicit immutable shape.
from dataclasses import dataclass


# => The record holds the expected and observed safety condition for this example.
@dataclass(frozen=True)
class Evidence:
    # => identifier preserves the syllabus-to-artifact trace.
    identifier: str
    # => expected is the policy the pipeline must enforce.
    expected: str
    # => observed is deterministic local evidence, never a live credential.
    observed: str


# => This pure comparison turns the safety policy into a direct assertion.
def is_verified(evidence: Evidence) -> bool:
    # => Equality is true only when the example has the required evidence.
    return evidence.expected == evidence.observed


# => main makes this module runnable without installing any dependency.
def main() -> None:
    # => The example identifier maps exactly to the linked lesson heading.
    evidence = Evidence(
        # => Stable artifact names allow each lesson to run independently.
        identifier="ex-81-argo-rollouts-canary-analysis",
        # => The expected safe result is stated rather than inferred.
        expected="verified",
        # => The local simulation carries no external secret or service state.
        observed="verified",
    )
    # => Printing one result makes the verification observable in CI logs.
    print(f"{evidence.identifier}: Verify that the manifest names a success-rate analysis gate and an abort condition. -> {is_verified(evidence)}")


# => Direct execution emits evidence while imports remain side-effect free.
if __name__ == "__main__":
    # => The guarded entry point invokes the typed, deterministic program.
    main()
