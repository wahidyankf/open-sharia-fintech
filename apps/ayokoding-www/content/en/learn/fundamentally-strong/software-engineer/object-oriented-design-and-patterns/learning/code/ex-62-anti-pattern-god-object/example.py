"""Example 62: Anti-Pattern -- God Object.

co-34 (anti-pattern recognition): a god object is diagnosed by a simple, objective
metric -- the number of DISTINCT responsibilities (unrelated method groups) a single
class carries -- and a fix is sketched (not fully executed here; Example 61 executes
the equivalent fix for a smaller case) as "split by reason-to-change."
"""

from __future__ import annotations


# => this class deliberately mixes concerns to demonstrate the smell -- Example 61 shows the same smell fixed
class ApplicationManager:  # => a god object: user auth, email sending, AND report generation, all in one class
    def __init__(self) -> None:  # => sets up state for TWO of the three responsibilities this god object carries
        self.users: dict[str, str] = {}  # => username -> password, for AUTH
        self.sent_emails: list[str] = []  # => log of sent emails, for EMAIL

    # => below: two methods share the SAME state (self.users) -- a genuine, cohesive AUTH pair
    def register_user(self, username: str, password: str) -> None:  # => AUTH responsibility
        self.users[username] = password  # => mutates the AUTH state dict directly

    def authenticate(self, username: str, password: str) -> bool:  # => AUTH responsibility
        return self.users.get(username) == password  # => reads the same AUTH state dict to check credentials

    # => this method touches a DIFFERENT piece of state (self.sent_emails) than the two AUTH methods above
    def send_email(self, to: str, subject: str) -> None:  # => EMAIL responsibility, unrelated to auth
        self.sent_emails.append(f"{to}:{subject}")  # => mutates the EMAIL state list, a completely different concern

    # => this method touches NEITHER self.users NOR self.sent_emails -- it is a pure function bolted onto the class
    def generate_report(self, title: str, rows: list[str]) -> str:  # => REPORTING responsibility, unrelated to both
        return f"# {title}\n" + "\n".join(rows)


# => this function is the "objective metric" the docstring promises: it counts concerns, not lines of code
def count_distinct_responsibilities(cls: type) -> int:  # => a simple, mechanical god-object detector
    method_prefixes = {  # => groups methods by a naming-convention proxy for "responsibility"
        "register_user": "auth",  # => maps each method name to the concern it actually serves
        "authenticate": "auth",  # => a second AUTH-concern method
        "send_email": "email",  # => the EMAIL-concern method
        "generate_report": "reporting",  # => the REPORTING-concern method
    }  # => closes the method-to-concern mapping dict
    methods_on_class = [name for name in method_prefixes if hasattr(cls, name)]  # => which of these methods exist
    concerns = {method_prefixes[name] for name in methods_on_class}  # => the DISTINCT concerns those methods serve
    return len(concerns)  # => 1 concern = cohesive class; 2+ = candidate god object


# => intentionally a sketch, not a real refactor: Example 61 shows the equivalent split fully executed and tested
def sketch_fix() -> list[str]:  # => the fix is SKETCHED here (named responsibilities), not fully executed
    return [  # => opens the list of sketched, human-readable split targets
        "AuthService: register_user(), authenticate() -- owns self.users",  # => split 1
        "EmailService: send_email() -- owns self.sent_emails",  # => split 2
        "ReportService: generate_report() -- owns nothing, pure function of its arguments",  # => split 3
    ]  # => closes the sketched-fix list


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    count = count_distinct_responsibilities(ApplicationManager)  # => the diagnostic metric
    print(count)  # => 3 distinct concerns in ONE class -- the god-object smell, named
    # => Output: 3
    # => count_distinct_responsibilities is deliberately crude (a naming-convention lookup), but names the smell
    for line in sketch_fix():  # => print the sketched split, one responsibility per line
        print(line)  # => prints one sketched responsibility split per line
    # => Output: AuthService: register_user(), authenticate() -- owns self.users
    # => Output: EmailService: send_email() -- owns self.sent_emails
    # => Output: ReportService: generate_report() -- owns nothing, pure function of its arguments
