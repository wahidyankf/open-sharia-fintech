"""Example 19: `Condition` -- wait() and notify()."""  # => co-14: predicate-based wait/notify coordination

import threading  # => threading.Condition -- a lock PLUS a wait/notify queue built on top of it


def consumer(cond: threading.Condition, state: dict[str, bool], log: list[str]) -> None:
    # => state: the shared predicate to wait on; log: records this thread's progress
    with cond:  # => Condition wraps a Lock -- `with` acquires it before touching shared `state`
        while not state["ready"]:  # => a LOOP, not an `if` -- guards against spurious wakeups (co-14)
            log.append("consumer-waiting")  # => recorded each time this thread goes back to sleep
            cond.wait()  # => atomically RELEASES the lock and blocks, until notified AND re-acquires
        log.append("consumer-woke")  # => only reached once state["ready"] is actually True


def producer(cond: threading.Condition, state: dict[str, bool], log: list[str]) -> None:
    # => uses the SAME cond/state/log objects the consumer above was given
    with cond:  # => must hold the SAME lock to safely mutate `state` and to call notify()
        state["ready"] = True  # => flips the shared predicate the consumer is waiting on
        log.append("producer-set-ready")  # => recorded right before waking the consumer
        cond.notify()  # => wakes ONE thread blocked in cond.wait() -- it re-acquires the lock and resumes


if __name__ == "__main__":  # => module entry point
    condition = threading.Condition()  # => a fresh Condition, wrapping its own internal Lock
    shared_state = {"ready": False}  # => the predicate consumer/producer coordinate around
    trace: list[str] = []  # => records the interleaved sequence of events, in actual order
    t_consumer = threading.Thread(target=consumer, args=(condition, shared_state, trace))
    # => t_consumer: will block in cond.wait() until the producer sets the predicate
    t_producer = threading.Thread(target=producer, args=(condition, shared_state, trace))
    # => t_producer: will flip shared_state["ready"] and notify() the waiting consumer
    t_consumer.start()  # => starts first -- almost certainly reaches cond.wait() before the producer runs
    t_producer.start()  # => sets ready=True and notifies once running
    t_consumer.join()  # => blocks until the consumer wakes and finishes
    t_producer.join()  # => blocks until the producer finishes

    print(trace)  # => Output: ['consumer-waiting', 'producer-set-ready', 'consumer-woke']
    # => the `while`, not `if`, guard matters even here -- see ex-74 for what breaks without it.
    assert "consumer-woke" in trace  # => confirms the consumer eventually woke up
    assert trace.index("producer-set-ready") < trace.index("consumer-woke")  # => notify happened BEFORE wake
    print("ex-19 OK")  # => Output: ex-19 OK
