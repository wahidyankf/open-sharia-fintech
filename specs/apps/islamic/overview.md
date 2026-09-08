# Islamic Tools — Product Overview

## Islamic BE (`islamic-be`)

A general-purpose Sharia-compliance API. It exists to serve any consumer that needs an
Islamic-finance or Sharia-compliance judgement — the OSE Application is expected to be one caller,
not the owner.

### Who uses it

- **Product engineers** integrating a compliance judgement into their own service
- **System operators** who need a liveness signal before routing traffic to an instance

### Scope

- A versioned HTTP surface under `/api/v1/`
- A contract-first specification that clients and the service both generate from
- A liveness probe operations can depend on

### What ships today

- `GET /api/v1/health` — the liveness probe, and nothing else

The service is deliberately a skeleton at this stage. It establishes the language lane, the
contract pipeline, and the behaviour corpus so that the first real compliance capability lands on a
proven surface rather than alongside one.

### What is deferred

- Every domain capability. No Sharia-compliance rule is implemented yet.
- Persistence. The service holds no database and writes nothing.
- Authentication. The surface is unauthenticated because it exposes nothing to protect.

### Why its own product line

`domain:islamic` rather than `domain:ose` because the capability is generic. Binding it to the OSE
Application's domain would make every future consumer a dependant of a GRC product it does not use.
