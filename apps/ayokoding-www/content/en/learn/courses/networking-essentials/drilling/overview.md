---
title: "Overview"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 1
---

This page is the active-recall companion to the Networking Essentials learning track: four fixed
drills that force retrieval instead of passive re-reading. Work through them in order --
short-answer recall first, then scenario judgment, then hands-on implementation, then a checklist to
confirm real automaticity. Every answer is hidden in a `<details>` block; try each item yourself,
out loud or on paper, before opening it. Every prompt below uses its own mocked, self-contained
input -- different hostnames, ports, and scenarios from anything in the learning track's 82 worked
examples -- so recognizing an answer isn't enough; you have to actually reconstruct the reasoning.

## Recall Q&A

Twenty-three short-answer questions, one per concept (`co-01` through `co-23`). Answer from memory,
then check.

**Q1 (co-01 -- client-server-model).** In one sentence, define the two roles every exchange in this
topic has, and name which role a mobile app playing a video from a streaming service takes.

<details>
<summary>Answer</summary>

One side (the client) initiates a request; the other (the server) listens and responds. The mobile
app is the client -- it initiates each request for the next chunk of video; the streaming service's
infrastructure is the server, listening and responding to those requests.

</details>

**Q2 (co-02 -- url-anatomy).** Break `https://api.example.org:8443/v2/orders?status=open` into its
five named components.

<details>
<summary>Answer</summary>

scheme = `https`, host = `api.example.org`, port = `8443` (explicit here, not defaulted), path =
`/v2/orders`, query = `status=open`. Each component routes the request differently: scheme picks
the protocol (and default port, if none given), host picks the machine, port picks the service on
that machine, path picks the resource, and query supplies extra parameters.

</details>

**Q3 (co-03 -- dns-resolution).** Before a browser can open any connection to `shop.example.net`,
what must happen first, and what does that step actually translate?

<details>
<summary>Answer</summary>

DNS resolution must happen first -- translating the hostname `shop.example.net` into an IP address
a network can actually route packets to. No TCP connection can open, and no HTTP request can be
sent, until this name-to-address translation completes.

</details>

**Q4 (co-04 -- dns-record-types).** A teammate says "the DNS record shows the mail server for our
domain." Which record type are they describing, and name two other record types that answer
different questions entirely.

<details>
<summary>Answer</summary>

They mean an `MX` record. `A`/`AAAA` records answer "what IP address does this name resolve to?"
and `NS` records answer "which servers are authoritative for this domain?" -- three different
questions, three different record types, all queryable independently for the same domain.

</details>

**Q5 (co-05 -- ip-and-ports).** A log line reads `connection to 203.0.113.9:22 refused`. Without
looking anything up, what service was almost certainly being attempted, and how do you know?

<details>
<summary>Answer</summary>

SSH -- port 22 is IANA's well-known port for SSH. Recognizing well-known ports (80 HTTP, 443 HTTPS,
22 SSH, 53 DNS) on sight is exactly the fluency this topic builds, so a bare port number in a log
line is immediately readable as "which service" without a lookup table.

</details>

**Q6 (co-06 -- icmp-ping).** `ping` reports 0% packet loss and consistent round-trip times against
a host. What does this confirm, and what does it deliberately NOT confirm?

<details>
<summary>Answer</summary>

It confirms the host is reachable at the network layer and responding to ICMP Echo Requests. It
does NOT confirm any application (a web server, a database) is actually listening on any specific
port -- `ping`'s ICMP exchange is completely independent of any application protocol.

</details>

**Q7 (co-07 -- tcp-connection).** Name the three steps of TCP's handshake, in order, and the one
guarantee this handshake sets up that a connectionless protocol cannot offer.

<details>
<summary>Answer</summary>

SYN, SYN-ACK, ACK. Once established, TCP delivers a reliable, ordered byte stream -- every byte
sent arrives, in the exact order sent, or the connection reports an error -- a guarantee a
connectionless protocol like UDP does not make.

</details>

**Q8 (co-08 -- udp-datagram).** A teammate sends a UDP datagram to a port with nothing listening.
What error does `sendto()` raise, and why?

<details>
<summary>Answer</summary>

None -- `sendto()` succeeds instantly with no error at all. UDP has no handshake to fail during; the
datagram is simply fired onto the wire. The only way to detect "nobody answered" is a timeout on the
receiving side, since UDP itself provides no delivery confirmation.

</details>

**Q9 (co-09 -- tcp-vs-udp).** A teammate is building a live video call feature and asks whether to
use TCP or UDP. What's the one-sentence tradeoff you'd explain?

<details>
<summary>Answer</summary>

TCP trades latency for reliability and ordering (every frame arrives, in order, but a lost packet
stalls everything waiting for retransmission); UDP trades those guarantees for low-overhead speed
(a dropped frame is just briefly skipped, which usually matters less for live audio/video than
waiting for it to be resent).

</details>

**Q10 (co-10 -- sockets-api).** Name the exact sequence of Berkeley sockets calls a TCP SERVER makes
before it can accept its first client, in order.

<details>
<summary>Answer</summary>

`socket()` (create it), `bind()` (claim an address/port), `listen()` (flip it passive, with a
backlog), `accept()` (block until a client's handshake completes). Skipping any step out of order
raises an error -- for instance, calling `accept()` before `listen()` fails immediately.

</details>

**Q11 (co-11 -- request-response-framing).** A raw TCP byte stream has no message boundaries at
all. Name one concrete way an application-level protocol can frame its messages anyway.

<details>
<summary>Answer</summary>

A delimiter (like `\n` for a line-based protocol) that the reader scans for, buffering bytes across
possibly many small `recv()` calls until the delimiter appears. An alternative is a fixed-size or
length-prefixed message, read with a loop that keeps calling `recv()` until exactly that many bytes
have arrived.

</details>

**Q12 (co-12 -- http-request-structure).** Name the four parts of an HTTP/1.1 request, in the order
they appear on the wire.

<details>
<summary>Answer</summary>

Request line (method, path, version), headers (zero or more, one per line), a blank line, then an
optional body. The blank line is the fixed boundary separating headers from body -- it's present
even when there is no body at all.

</details>

**Q13 (co-13 -- http-response-structure).** A response begins `HTTP/1.1 404 Not Found`. Name each of
the three pieces in that one line.

<details>
<summary>Answer</summary>

`HTTP/1.1` is the protocol version, `404` is the numeric status code, `Not Found` is the human-
readable reason phrase. This status line is followed by headers, a blank line, and an optional body
-- the response's mirror of the request line's fixed structure.

</details>

**Q14 (co-14 -- http-methods).** Match each of `GET`, `POST`, `PUT`, `DELETE`, and `HEAD` to its
core semantic intent in one short phrase each.

<details>
<summary>Answer</summary>

`GET` reads a resource; `POST` creates or submits data; `PUT` replaces a resource entirely; `DELETE`
removes a resource; `HEAD` runs the same logic as `GET` but returns headers only, no body.

</details>

**Q15 (co-15 -- http-status-codes).** A monitoring dashboard shows a spike in `5xx` responses. Is
this most likely a client-side bug or a server-side problem, and how does that differ from a spike
in `4xx`?

<details>
<summary>Answer</summary>

`5xx` signals a server-side problem -- the request was probably fine, and retrying later might
succeed. A `4xx` spike signals the REQUESTS themselves are likely malformed or invalid -- retrying
the exact same request unchanged won't help; the client (or the caller sending it) needs to change
something first.

</details>

**Q16 (co-16 -- http-headers).** Name the specific header that tells a client how many bytes to
expect in a response body, and the specific header that tells a server which of possibly many
hosted sites a request is for.

<details>
<summary>Answer</summary>

`Content-Length` states the body's byte size; `Host` names which site/domain the request targets --
required in HTTP/1.1 because one server can host many domains behind the same IP address.

</details>

**Q17 (co-17 -- http-vs-https-tls).** In one sentence, what does HTTPS add on top of plain HTTP, and
what port does it default to?

<details>
<summary>Answer</summary>

HTTPS wraps the exact same HTTP request/response exchange inside a TLS session that encrypts and
authenticates the connection; it defaults to port 443, versus HTTP's port 80.

</details>

**Q18 (co-18 -- redirects).** A response has status `301` and a `Location` header. What should a
well-behaved client do next?

<details>
<summary>Answer</summary>

Issue a new request to the URL named in the `Location` header -- a `3xx` status is specifically the
server's way of saying "the resource you want is somewhere else; go there instead," and `Location`
names exactly where.

</details>

**Q19 (co-19 -- curl-tooling).** Which single curl flag turns on the full protocol trace (TLS
handshake, sent request lines, received response lines), and which flag restricts a request to
headers only, no body?

<details>
<summary>Answer</summary>

`-v` (verbose) prints the full trace; `-I` sends a `HEAD` request, returning headers with no body.

</details>

**Q20 (co-20 -- dns-tooling).** Name three different command-line tools that can each independently
confirm what IP address a hostname resolves to.

<details>
<summary>Answer</summary>

`dig`, `nslookup`, and `host` -- three separate tools, all capable of querying DNS directly and
reporting the resolved address, useful when confirming one tool's answer against an independent
second source.

</details>

**Q21 (co-21 -- connection-inspection).** What can `nc` (netcat) do that `curl` cannot, when it
comes to inspecting raw protocol bytes?

<details>
<summary>Answer</summary>

`nc` sends or receives completely raw TCP bytes with zero protocol logic of its own -- no request
parsing, no response parsing. This makes it possible to see the EXACT bytes a client sends (by
listening with `nc -l`) or to hand-type completely arbitrary bytes to a server, neither of which
`curl`'s built-in HTTP logic allows.

</details>

**Q22 (co-22 -- content-negotiation).** A client sends `Accept: application/json` in its request.
What is the server expected to do with that header, and name the response header that confirms it
complied?

<details>
<summary>Answer</summary>

The server is expected to choose a representation matching the client's stated preference (JSON,
here) if it can. The response's `Content-Type` header confirms which representation the server
actually chose to send back.

</details>

**Q23 (co-23 -- stdlib-http-client).** Name Python's two standard-library HTTP client interfaces
covered in this topic, and the one key difference in how each is invoked.

<details>
<summary>Answer</summary>

`http.client` (lower-level: separate host/port and path arguments, an explicit connection object)
and `urllib.request` (higher-level: takes one full URL string and parses it internally). Both
expose the same essential status/headers/body once a response comes back.

</details>

## Applied problems

Twelve scenarios spanning beginner through advanced material. Each describes a realistic
engineering situation without naming the specific tool or technique -- decide what applies and why,
then check your reasoning against the worked solution.

**AP1.** A teammate reports "the checkout page is down" but gives no other detail. What are the
first two commands you'd run, and what does each one rule in or out?

<details>
<summary>Worked solution</summary>

`ping <host>` rules network-layer reachability in or out, independent of any application; `curl -v
<url>` (or `curl -I <url>`) rules the actual HTTP exchange in or out, showing the real status code
and headers. Running both quickly separates "the whole host is unreachable" from "the host answers,
but something in the HTTP layer (or above) is broken" (co-06, co-19).

</details>

**AP2.** A new service's health-check endpoint returns `200 OK` from `curl`, yet the on-call
engineer insists "the site is completely broken for users." What's a plausible explanation that
doesn't contradict either observation?

<details>
<summary>Worked solution</summary>

The health-check endpoint and the actual user-facing endpoint(s) are different resources -- a `200`
on `/healthz` says nothing about `/checkout` or `/api/orders`. Also worth checking: is `curl`
reaching the SAME backend instance/region users are hitting, or a different one behind a load
balancer (co-01, co-15)?

</details>

**AP3.** You need to confirm whether a domain's mail is hosted by a third-party provider (like a
dedicated email service) rather than the same infrastructure serving its website. Which DNS record
type answers this directly?

<details>
<summary>Worked solution</summary>

`MX` -- it names the mail server(s) responsible for the domain, completely independent of whatever
`A`/`AAAA` records point the website itself at (co-04).

</details>

**AP4.** A client reports "your API returned an error, but retrying the exact same request five
minutes later worked fine." Which status class does this best fit, and why would you NOT expect
retrying to help for the other main error class?

<details>
<summary>Worked solution</summary>

This fits `5xx` -- a transient server-side problem that could plausibly resolve itself. A `4xx`
error means something about the REQUEST itself is wrong (bad auth, malformed body, missing
parameter); retrying the identical request changes nothing about that underlying problem (co-15).

</details>

**AP5.** A request to `http://internal-api/orders` succeeds, but the identical path over
`https://internal-api/orders` fails with a connection-level error, not an HTTP-level one. What's the
first thing to check?

<details>
<summary>Worked solution</summary>

Whether the server on port 443 is actually configured to speak TLS at all -- a plaintext request to
a TLS-expecting port (or, less commonly, a certificate/handshake misconfiguration) produces exactly
this pattern: port 80 answers normally, port 443 rejects at the connection or handshake level before
any HTTP semantics are even reached (co-17).

</details>

**AP6.** A frontend team says a redirect chain "loses" a custom header they set on the original
request. Why would that happen, and is it a bug in their HTTP client?

<details>
<summary>Worked solution</summary>

Not necessarily a bug -- a redirect (`3xx` + `Location`) is a genuinely SEPARATE second request to a
possibly different host, and most HTTP client libraries do not automatically re-attach custom
headers (especially sensitive ones like `Authorization`) to that second request by default, for
security reasons. The fix is to re-set the header explicitly when following the redirect manually
(co-18).

</details>

**AP7.** A backend team wants to log exactly which bytes a mobile client sends in its request,
including any malformed ones a buggy client version might be producing, without relying on the
server's own (possibly buggy) request parser. What tool fits, and why not the server's own logs?

<details>
<summary>Worked solution</summary>

`nc -l <port>`, pointed at temporarily -- it captures the exact, raw, unparsed bytes as they arrive,
with zero interpretation. The server's own logs only show what its parser successfully understood,
which is exactly the blind spot when the SUSPECTED bug is in that parser itself (co-21).

</details>

**AP8.** An API needs to serve both a JSON payload for programmatic clients and an HTML page for
browsers, from the exact same URL. What mechanism lets one endpoint serve both, and what decides
which one a given request gets?

<details>
<summary>Worked solution</summary>

Content negotiation via the request's `Accept` header -- the server reads it and picks
`Content-Type: application/json` or `Content-Type: text/html` accordingly, confirmed by the
response's own `Content-Type` header (co-22).

</details>

**AP9.** A service needs to handle thousands of simultaneous, mostly-idle client connections (like
a chat application) as cheaply as possible. Would a thread-per-client design (like this topic's
examples) scale well here, and what's the general tradeoff?

<details>
<summary>Worked solution</summary>

A pure thread-per-client design (this topic's teaching pattern) works for modest concurrency but
scales poorly into the thousands, since each OS thread carries real memory/scheduling overhead --
production systems at that scale typically use event-loop or async I/O models instead. The
underlying socket concepts (bind/listen/accept, framing, the request/response shape) stay identical
either way; only the CONCURRENCY strategy changes (co-10).

</details>

**AP10.** A client library sends a request and hangs indefinitely when the target host is
unreachable, with no way for a caller to bound how long it waits. What's the fix, and what specific
exception should the caller be prepared to catch?

<details>
<summary>Worked solution</summary>

Set an explicit connect timeout on the socket/client (most stdlib and third-party HTTP clients
accept a `timeout` parameter). The caller should be prepared to catch a timeout-specific exception
(`TimeoutError` in Python's `socket` module) distinct from a `ConnectionRefusedError`, since an
unreachable host produces silence, not an active rejection (co-10).

</details>

**AP11.** A monitoring tool reports "50% of UDP-based telemetry packets never arrived" for one
service, while the equivalent TCP-based service reports zero loss. Is the UDP service necessarily
broken?

<details>
<summary>Worked solution</summary>

Not necessarily -- UDP provides no delivery guarantee at all, so SOME loss under load or on a lossy
network path is expected, unlike TCP, which either delivers every byte or surfaces an error. Whether
50% is "broken" depends entirely on what the telemetry data is used for and what loss tolerance was
designed in from the start (co-08, co-09).

</details>

**AP12.** An engineer debugging a failed request sees only "connection failed" in a generic error
log, with no further detail. What's the fastest way to narrow down WHICH layer actually failed --
DNS, TCP, or the application protocol itself?

<details>
<summary>Worked solution</summary>

Break the exact same request into its stages by hand: first try resolving the hostname alone (does
DNS succeed?), then try a bare TCP connect to the resolved address and port (does the handshake
succeed?), then attempt the actual application-level exchange. Whichever stage first fails is where
the real problem sits -- exactly the `layering-and-leaks` idea this topic keeps returning to
(co-01, co-03, co-07).

</details>

## Code katas

Eight hands-on drills, spanning beginner tools through advanced socket work. Each is a
self-contained, runnable task with a scenario distinct from the learning track's 82 worked
examples -- reusing this topic's own `example.com`/`example.org`/`example.net` reproducibility
pattern wherever a live host is genuinely needed, per DD-30: attempt the task yourself first, then
compare against the reference approach and the genuinely captured output shown.

### Kata 1 -- Read a status line and one header from curl -v

**Task.** Run `curl -v --http1.1 https://example.com` and, from the verbose trace alone (no other
tool), report the response's status line and its `Content-Type` header value.

**Reference approach**: grep the `-v` trace for lines starting with `< HTTP` (the status line) and
`< Content-Type` (the header).

```bash
curl -v --http1.1 https://example.com 2>&1 1>/dev/null | grep -E "^< HTTP|^< Content-Type"
```

**Output** (genuinely captured):

```text
< HTTP/1.1 200 OK
< Content-Type: text/html
```

**Key takeaway**: The same `grep`-the-verbose-trace technique this topic used throughout Examples
1-28 works unchanged here -- extracting a status line and one header from a `-v` trace is a
host-agnostic skill. `example.com` is reused deliberately, not a fresh production host, so this
kata's captured output stays reproducible for every reader (DD-30) instead of drifting if a
third-party site ever changes its headers.

### Kata 2 -- Compare A and NS records for a different domain

**Task.** Run `dig +short example.org A` and `dig example.org NS`, and report how many A records and
how many nameservers each returns. (`example.org` is deliberately a different domain from Examples
11 and 15's `example.com`, so this kata still exercises the technique against fresh `dig` output
rather than recalling an already-memorized answer.)

**Output** (genuinely captured):

```text
$ dig +short example.org A
104.20.26.136
172.66.157.237

$ dig example.org NS
;; ANSWER SECTION:
example.org.  3500 IN NS mitch.ns.cloudflare.com.
example.org.  3500 IN NS katelyn.ns.cloudflare.com.
```

**Key takeaway**: `example.org` has two A records and two authoritative nameservers -- a concrete
reminder that "how many records" is answered independently per record TYPE (`dig ... A` says
nothing about how many NS records exist, and vice versa), not as one combined count for the whole
domain.

### Kata 3 -- Write your own `read_line()` framing helper

**Task.** Without looking at Example 33, write a `read_line(sock: socket.socket, buffer:
bytearray) -> bytes` function from memory that reassembles a `\n`-delimited line from possibly many
small `recv()` calls.

**Reference approach**:

```python
def read_line(sock: socket.socket, buffer: bytearray) -> bytes:
    while b"\n" not in buffer:
        chunk = sock.recv(4)  # tiny on purpose -- forces multiple reads to prove framing works
        if not chunk:
            raise ConnectionError("peer closed mid-line")
        buffer.extend(chunk)
    line, _, rest = buffer.partition(b"\n")
    buffer[:] = rest
    return bytes(line)
```

**Key takeaway**: The core structure -- loop until the delimiter is present, then split once and
keep the remainder -- is the entire idea; the read size (4 bytes here, versus Example 33's 4 bytes
or Example 35's 64 bytes) is an arbitrary implementation detail that doesn't change the logic at
all.

### Kata 4 -- Extend the PING/TIME protocol with an ECHO command

**Task.** Starting from Example 36's `handle_command()` shape, add a THIRD command, `ECHO <text>`,
that replies with exactly `<text>` unchanged. Write the branching logic (no need to run a full
server) and state what happens for an unrecognized command.

**Reference approach**:

```python
def handle_command(command: bytes) -> bytes:
    if command == b"PING":
        return b"PONG"
    if command == b"TIME":
        return str(int(time.time())).encode()
    if command.startswith(b"ECHO "):
        return command[len(b"ECHO "):]  # everything after "ECHO "
    return b"ERR unknown command: " + command
```

**Key takeaway**: Adding a new command is purely additive -- one more `if` branch, no change to
`read_line()`'s framing or the server's accept loop -- confirming the protocol layer (co-11, co-01)
and the transport/framing layer are genuinely decoupled from each other.

### Kata 5 -- Diagnose a DNS failure vs. a TCP failure, with fresh hosts

**Task.** Without reusing Example 80's exact hosts, pick a guaranteed-nonexistent hostname (any
`.invalid` name) and a guaranteed-closed local port, and write the two-step
try-DNS-then-try-TCP pattern that classifies which layer failed for each.

**Reference approach**: reuse Example 80's `classify_failure()` shape verbatim, but point it at
`totally-made-up-host.invalid` and `127.0.0.1:59999` (or any other unused local port) instead.

**Key takeaway**: The classification LOGIC (try `gethostbyname`, catch `socket.gaierror`; then try
`create_connection`, catch `ConnectionRefusedError`) is completely reusable across any pair of
hosts/ports -- it's a general debugging pattern, not something tied to one specific demo host.

### Kata 6 -- Time a DNS lookup against two different hosts

**Task.** Using `time.perf_counter()`, measure `socket.gethostbyname()`'s time for two DIFFERENT
real hosts and compare. This kata reuses `example.com` and `example.net` -- the same RFC
2606-reserved documentation domains this topic relies on everywhere else -- specifically so the
captured timings below stay reproducible for every reader, instead of drifting with a production
site's own infrastructure changes.

**Reference approach**:

```python
import socket
import time

for host in ("example.com", "example.net"):
    start = time.perf_counter()
    ip = socket.gethostbyname(host)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"{host} -> {ip} ({elapsed_ms:.1f} ms)")
```

**Output** (genuinely captured):

```text
example.com -> 172.66.147.243 (14.2 ms)
example.net -> 104.20.21.8 (3.1 ms)
```

**Key takeaway**: Two different, real hosts genuinely resolve in different amounts of time --
resolution speed depends on caching state and which resolvers are involved, not on some fixed "DNS
always takes X ms" constant; reusing this topic's reserved documentation domains here doesn't
change that this is a genuine, live DNS lookup against two distinct authoritative infrastructures.

### Kata 7 -- Send a UDP datagram to a well-known DNS resolver's port and observe

**Task.** Send a UDP datagram (arbitrary bytes, not a real DNS query) to `8.8.8.8:53` -- a real,
running DNS resolver's own port -- and observe what happens differently from sending to a genuinely
closed port.

**Reference approach**: reuse Example 56's `sendto()`/`recvfrom()` shape, but target `("8.8.8.8",
53)` instead of a closed local port, with a short timeout.

**Why a live host here, unlike Katas 1/2/6**: this kata's entire point is contrasting behavior
against a REAL, LISTENING third-party service with Example 56's closed-port case -- a mocked or
self-contained target cannot substitute for that, since a mock only ever reproduces whatever
behavior the reader coded into it, never a genuinely independent service's own error handling.
`8.8.8.8` (Google Public DNS) is chosen deliberately over an arbitrary production site: unlike
`www.iana.org`'s exact response headers or `wikipedia.org`'s exact record set, this kata asserts no
single specific byte-for-byte output (see the takeaway below), and `8.8.8.8` has been long-lived,
stable, well-known public infrastructure since 2009. This is a deliberate, scoped exception to this
topic's `example.com`/`example.org`/`example.net` reproducibility pattern, not an oversight.

**Key takeaway**: Sending malformed bytes to a REAL, listening UDP service (as opposed to a closed
port) can produce a range of outcomes depending on that service's own error handling -- reinforcing
that UDP's "no error on send" behavior (co-08) is a genuinely different debugging surface from TCP's
active `ConnectionRefusedError`.

### Kata 8 -- Build a one-off content-type-aware response by hand

**Task.** Without copying Example 51's server verbatim, write a small function `build_reply(accept:
str) -> bytes` that returns a full, valid `HTTP/1.1 200 OK` response (status line, `Content-Type`,
`Content-Length`, blank line, body) choosing between `text/plain` and `application/xml` based on
whether `"application/xml"` appears in `accept`.

**Reference approach**: the same status-line + headers + blank-line + body assembly Examples 41 and
51 both use, with a third possible `Content-Type` branch instead of two.

**Key takeaway**: Once the response-assembly SHAPE (status line, headers, blank line, body,
joined with `\r\n`) is memorized, extending it to a third content type is a one-line change to the
branching logic -- the wire format itself never changes.

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can name the two roles every exchange in this topic has and identify them in a real
      example without hesitation. (co-01)
- [ ] I can break any URL into scheme, host, port, path, and query, including when the port is
      only implicit. (co-02)
- [ ] I can explain why DNS resolution must happen before any connection opens. (co-03)
- [ ] I can name at least five DNS record types and the specific question each one answers.
      (co-04)
- [ ] I can name the four well-known ports this topic uses and their services, from memory. (co-05)
- [ ] I can explain what `ping` confirms and what it deliberately does not confirm about a host.
      (co-06)
- [ ] I can name TCP's three-way handshake steps in order and state the guarantee it sets up.
      (co-07)
- [ ] I can explain why `sendto()` never raises an error even when nothing is listening. (co-08)
- [ ] I can state the TCP-vs-UDP tradeoff in one sentence and give an example use case for each.
      (co-09)
- [ ] I can name the exact ordered sequence of socket calls a TCP server makes before its first
      `accept()`. (co-10)
- [ ] I can explain why a raw byte stream needs explicit message framing, and describe one framing
      technique. (co-11)
- [ ] I can name the four parts of an HTTP/1.1 request, in wire order. (co-12)
- [ ] I can name the three parts of an HTTP/1.1 status line and what each one means. (co-13)
- [ ] I can state the core semantic intent of `GET`, `POST`, `PUT`, `DELETE`, and `HEAD` without
      hesitation. (co-14)
- [ ] I can explain the practical difference between a `4xx` and a `5xx` response for a retry
      policy. (co-15)
- [ ] I can name `Host`, `Content-Type`, `Content-Length`, and `Accept` and what each one
      communicates. (co-16)
- [ ] I can explain what HTTPS adds on top of HTTP and its default port. (co-17)
- [ ] I can explain what a well-behaved client should do upon receiving a `3xx` with a `Location`
      header. (co-18)
- [ ] I can name at least four curl flags (`-v`, `-I`, `-L`, `-d`, `-H`, `-w`) and what each one
      does. (co-19)
- [ ] I can name three DNS command-line tools and use any one of them to resolve a hostname.
      (co-20)
- [ ] I can explain what `nc` can inspect that a protocol-aware client like `curl` cannot. (co-21)
- [ ] I can explain how `Accept` and `Content-Type` work together to negotiate a response's
      representation. (co-22)
- [ ] I can name Python's two stdlib HTTP client interfaces and the key difference in how each is
      invoked. (co-23)
- [ ] I can explain, in one sentence, what `layering-and-leaks` means for this topic -- name one
      real failure and which layer it actually surfaced from versus which layer actually broke.
      (`layering-and-leaks`)

---

← Previous: [Capstone](../learning/capstone/overview.md)
