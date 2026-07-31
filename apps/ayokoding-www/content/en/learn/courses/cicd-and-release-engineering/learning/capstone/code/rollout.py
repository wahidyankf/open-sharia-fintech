"""Local progressive-delivery and provenance simulation for the CI/CD capstone."""

# => argparse accepts an explicit simulated health value from CI or a local run.
import argparse

# => dataclass gives each candidate immutable, inspectable delivery evidence.
from dataclasses import dataclass


# => Candidate binds a single digest to health, signing, and provenance evidence.
@dataclass(frozen=True)
class Candidate:
    # => digest identifies the only artifact eligible for each promotion stage.
    digest: str
    # => health is the canary signal observed before wider exposure.
    health: str
    # => signed records whether signature verification succeeded.
    signed: bool
    # => attested records whether provenance verification succeeded.
    attested: bool


# => decide converts evidence into an explicit, side-effect-free rollout action.
def decide(candidate: Candidate) -> str:
    # => Missing supply-chain evidence blocks promotion before traffic changes.
    if not candidate.signed or not candidate.attested:
        # => The candidate has no trustworthy identity, so it cannot deploy.
        return "block"
    # => An unhealthy canary restores the known-good route immediately.
    if candidate.health != "healthy":
        # => The narrow audience stays narrow when health evidence fails.
        return "rollback"
    # => Verified, healthy evidence permits the next progressive-delivery stage.
    return "promote"


# => parse_args constrains the local simulation to two observable health states.
def parse_args() -> argparse.Namespace:
    # => ArgumentParser gives the command a discoverable and safe interface.
    parser = argparse.ArgumentParser()
    # => The default makes the green path runnable without extra configuration.
    parser.add_argument("--health", choices=("healthy", "unhealthy"), default="healthy")
    # => Parsed arguments select deterministic evidence rather than a cloud API call.
    return parser.parse_args()


# => main creates the candidate once and reports the policy decision.
def main() -> None:
    # => The command-line health signal drives the promotion or rollback outcome.
    arguments = parse_args()
    # => This digest and its evidence are examples, never a real registry artifact.
    candidate = Candidate("sha256:demo-candidate", arguments.health, signed=True, attested=True)
    # => The line records the exact evidence chain a reviewer needs to inspect.
    print(f"digest={candidate.digest} health={candidate.health} action={decide(candidate)}")


# => The guard supports direct execution while keeping imports side-effect free.
if __name__ == "__main__":
    # => Direct invocation produces one deterministic rollout decision.
    main()
