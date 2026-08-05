# Actor model and CSP in the capstone

The capstone service owns its state in a GenServer and is addressed through a Registry name. Clients send
requests to that identity; they do not share the state. Its supervisor restarts a crashing worker, so
recovery is a property of the tree.

The CSP counterpart would model work through channels. An unbuffered channel rendezvous makes demand and
back-pressure explicit, while cancellation, shutdown, and recovery must be coordinated by the program.

Use this actor design when a named service should retain an isolated lifecycle and restart boundary. Use
CSP when a bounded hand-off pipeline is the central design concern.
