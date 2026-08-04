# Actor model and CSP

Elixir actors are addressed by process identity: sending is asynchronous, so the sender continues while
the receiver's mailbox absorbs work. OTP supervision gives the actor side a built-in recovery boundary.
This suits independent services whose failures should be isolated and restarted.

Go-style CSP coordinates anonymous goroutines through channels. An unbuffered send synchronizes with a
receiver, so the rendezvous directly expresses back-pressure and ordering, but cancellation, lifecycle,
and recovery remain explicit responsibilities of the program.

Choose actors for identity-addressed, failure-isolated services; choose CSP when synchronous hand-off and
explicit coordination make the data-flow easier to reason about.
