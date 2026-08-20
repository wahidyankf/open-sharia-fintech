# Testing Methodology — Session-Based Exploratory Testing

Structure the work as one or more **time-boxed charters** (Session-Based Test Management). Each
charter is a focused mission; opportunistic findings outside the charter are still recorded.

## 1. Frame charters

Use Elisabeth Hendrickson's template:

```
Explore <endpoint / operation / resource / risk>
With   <method / payloads / auth contexts / contract / restrictions>
To discover <information / risk class / quality attribute>
```

Derive charters from the goal. Example for "verify the activities REST endpoints":

- `Explore POST /activities with boundary and malformed payloads (empty, missing required, wrong
types, oversized, Unicode) to discover validation and error-envelope defects.`
- `Explore GET /activities pagination + filtering across page boundaries and invalid params to
discover contract-conformance defects against openapi.yaml.`

## 2. Apply tours to vary the angle of attack

Adapt James Whittaker's tour taxonomy to an API:

- **Money / Landmark tour** — the documented, primary operations in varying order.
- **FedEx tour** — the data lifecycle across endpoints: create → read → update → list → delete; assert
  the resource is consistent at each hop.
- **Antisocial / Intellectual tour** — invalid, out-of-order, boundary, and malformed requests;
  wrong content-type; missing/extra fields; nonsensical pagination cursors.
- **Configuration tour** — content negotiation, `Accept`/`Content-Type` variants, API version headers.
- **Obsessive-Compulsive tour** — repeat the same write (idempotency), replay the same request
  (caching, rate-limit, duplicate-side-effect).
- **Back Alley tour** — least-used operations, optional parameters, deprecated fields.

## 3. Cover the product surface with SFDIPOT

Sweep the "San Francisco Depot" heuristic, adapted to an API, so coverage is not accidental:

- **S**tructure — every documented path/operation, resource, and schema component.
- **F**unction — what each operation does; the returned representation; computed/derived fields.
- **D**ata — request/response payloads: boundaries, nulls, missing/extra fields, wrong types, special
  chars, Unicode/emoji, very large values, numeric overflow, encodings, date/time formats.
- **I**nterfaces — status codes, headers, error envelopes, pagination/cursor contracts, links/HATEOAS,
  downstream/3rd-party calls visible in the response.
- **P**latform — auth scheme, content negotiation, API version, rate-limit headers.
- **O**perations — real client journeys across endpoints, error recovery, retry/idempotency behaviour.
- **T**ime — token/session expiry, ordering, concurrency/race on the same resource, debounce/rate-limit
  windows, date/time edge cases (timezone/DST), perceived latency.

## 4. Judge against quality criteria (CRUSSPIC STMPL)

Probe Capability, Reliability, Usability (API ergonomics / contract clarity), Security, Scalability,
Performance, Compatibility — and Supportability, Testability, Maintainability, Portability,
Localizability where observable. Most API charters lean on Capability, Reliability, Security,
Performance, and Compatibility (contract conformance).
