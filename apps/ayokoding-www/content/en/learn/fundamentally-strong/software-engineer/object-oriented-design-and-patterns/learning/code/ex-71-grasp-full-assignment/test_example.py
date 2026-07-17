"""Example 71: pytest verification that each of the nine GRASP patterns is placed correctly."""

from datetime import timedelta

from example import (
    Library,
    LibraryController,
    LoanRepository,
    PremiumFeePolicy,
    StandardFeePolicy,
    make_logging_notifier,
)


def test_information_expert_loan_computes_its_own_fee() -> None:
    repository = LoanRepository()
    library = Library(repository)
    loan = library.checkout("Clean Code", "Ada", StandardFeePolicy())  # => Loan owns due_date, computes its own fee
    later = loan.due_date + timedelta(days=4)
    assert loan.fee(later) == 1.0  # => 4 days overdue * $0.25/day


def test_creator_library_creates_its_own_loans() -> None:
    repository = LoanRepository()
    library = Library(repository)
    loan = library.checkout("Refactoring", "Grace", StandardFeePolicy())
    assert loan in repository.all()  # => the creation method lives on Library, not scattered elsewhere


def test_controller_routes_the_checkout_request_so_the_ui_never_touches_library_directly() -> None:
    repository = LoanRepository()
    library = Library(repository)
    controller = LibraryController(library)
    loan = controller.handle_checkout_request("Domain-Driven Design", "Eric", is_premium=True)
    assert loan.book_title == "Domain-Driven Design"  # => reached the domain only through the controller


def test_polymorphism_premium_and_standard_policies_dispatch_differently() -> None:
    repository = LoanRepository()
    library = Library(repository)
    standard_loan = library.checkout("Book A", "Bob", StandardFeePolicy())
    premium_loan = library.checkout("Book B", "Cate", PremiumFeePolicy())
    later = standard_loan.due_date + timedelta(days=10)
    assert standard_loan.fee(later) > premium_loan.fee(later)  # => same days overdue, different rate, no type-switch


def test_pure_fabrication_repository_keeps_library_io_free() -> None:
    repository = LoanRepository()
    assert not hasattr(Library(repository), "_loans")  # => Library never holds raw persistence state itself


def test_low_coupling_and_indirection_notifier_fires_without_a_concrete_reference() -> None:
    log: list[str] = []
    repository = LoanRepository()
    library = Library(repository, on_overdue=make_logging_notifier(log))  # => Library only knows a callable exists
    loan = library.checkout("Overdue Book", "Dan", StandardFeePolicy())
    past_due = loan.due_date + timedelta(days=1)
    library.check_for_overdue(past_due)
    assert log == ["Dan is overdue on Overdue Book"]  # => the mediator/callback fired, decoupled from any class name


def test_high_cohesion_loan_methods_touch_only_its_own_fields() -> None:
    loan = Library(LoanRepository()).checkout("Book C", "Eve", StandardFeePolicy())
    assert loan.days_overdue(loan.due_date) == 0  # => not yet due
    assert loan.days_overdue(loan.due_date + timedelta(days=3)) == 3  # => uses only its own due_date


def test_protected_variations_swapping_the_fee_policy_needs_no_loan_edit() -> None:
    repository = LoanRepository()
    library = Library(repository)
    loan = library.checkout("Book D", "Frank", PremiumFeePolicy())  # => a DIFFERENT policy, same Loan class
    assert loan.fee_policy.daily_rate() == 0.10  # => the swap is transparent through the FeePolicy interface


# => Run: pytest -q -- Output: 8 passed
