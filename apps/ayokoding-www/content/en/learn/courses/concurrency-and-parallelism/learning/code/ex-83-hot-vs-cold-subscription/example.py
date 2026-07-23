"""Example 83: Cold Observables Replay in Full; Hot Subjects Drop What Already Happened."""

import reactivex  # => co-31: `reactivex.from_iterable` (cold) vs `Subject` (hot) behave very differently
from reactivex.subject import Subject  # => Subject: BOTH an Observable AND an Observer -- the "hot" primitive


def cold_observable_demo() -> tuple[list[int], list[int]]:
    cold = reactivex.from_iterable(range(5))  # => cold: a COLD Observable -- produces nothing until subscribed
    first_results: list[int] = []  # => first_results: filled in by the FIRST subscription
    second_results: list[int] = []  # => second_results: filled in by a SECOND, later subscription
    cold.subscribe(on_next=first_results.append)  # => this subscription runs the WHOLE sequence, start to finish
    cold.subscribe(on_next=second_results.append)  # => a LATE subscriber still gets the ENTIRE sequence, independently
    return first_results, second_results  # => both should be IDENTICAL -- cold replays in full, every time


def hot_subject_demo() -> tuple[list[int], list[int]]:
    subject: Subject[int] = Subject()  # => subject: a HOT source -- emissions happen regardless of who's listening
    early_results: list[int] = []  # => early_results: filled in by a subscriber that joined BEFORE any emissions
    late_results: list[int] = []  # => late_results: filled in by a subscriber that joins AFTER some emissions
    subject.subscribe(on_next=early_results.append)  # => subscribes FIRST -- will see EVERY emission from now on

    subject.on_next(1)  # => pushes 1 -- ONLY early_results (the current subscriber) sees it
    subject.on_next(2)  # => pushes 2 -- ONLY early_results sees it, since late hasn't subscribed yet

    subject.subscribe(on_next=late_results.append)  # => subscribes LATE -- AFTER 1 and 2 already happened
    subject.on_next(3)  # => pushes 3 -- BOTH early_results and late_results see this one
    subject.on_next(4)  # => pushes 4 -- BOTH see this one too

    return early_results, late_results  # => early sees everything; late MISSES whatever fired before it joined


if __name__ == "__main__":  # => module entry point
    cold_first, cold_second = cold_observable_demo()  # => drives the cold-Observable scenario
    print(f"cold_first={cold_first} cold_second={cold_second}")  # => Output: cold_first=[0,1,2,3,4] cold_second=[0,1,2,3,4]

    hot_early, hot_late = hot_subject_demo()  # => drives the hot-Subject scenario
    print(f"hot_early={hot_early} hot_late={hot_late}")  # => Output: hot_early=[1,2,3,4] hot_late=[3,4]

    # => A COLD Observable (like `from_iterable`) has no state of its own -- each `.subscribe()` call
    # => independently starts the SAME production from the beginning, so a "late" subscriber sees the
    # => full sequence just like the first one did (co-31). A HOT `Subject` is different: it's a live
    # => broadcast -- emissions happen the instant `.on_next()` is called, REGARDLESS of who's currently
    # => subscribed. A subscriber joining late has simply MISSED whatever already happened; there is no
    # => replay unless you explicitly reach for a `ReplaySubject` instead of a plain `Subject`.
    assert cold_first == list(range(5))  # => confirms the first cold subscriber got the full sequence
    assert cold_second == cold_first  # => confirms the LATE cold subscriber got the IDENTICAL full sequence
    assert hot_early == [1, 2, 3, 4]  # => confirms the early hot subscriber saw EVERY emission
    assert hot_late == [3, 4]  # => confirms the late hot subscriber MISSED the emissions before it joined
    print("ex-83 OK")  # => Output: ex-83 OK
