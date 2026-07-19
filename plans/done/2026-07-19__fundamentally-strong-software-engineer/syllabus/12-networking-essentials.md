# 12 · Networking Essentials (By Example, Python)

**prd row**: Pass 1 · Core Foundations · By Example · Python · Learn 112 / Drill 212 · Nvim-ready
Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the **usable slice** — what happens when you hit a URL, HTTP in practice, DNS, and a
sockets intro, all from the terminal. OSI layering, subnetting, congestion control, HTTP/2-3, and
`tcpdump` analysis go to [`29-advanced-networking`](./29-advanced-networking.md) (DD-11).

## Why this exists · the big idea

- **The problem before the solution**: your software talks to other machines constantly, and when it
  breaks you must know what happens between "hit a URL" and "get a response" — otherwise every network bug
  is magic.
- **Keep-this-if-you-forget-everything**: the network is a stack of translations — name → address →
  connection → bytes → message (DNS → TCP → TLS → HTTP) — and you debug by asking which layer failed.
- **Big ideas touched**: `layering-and-leaks` — each layer hides the one below until it leaks (a DNS
  failure surfaces as an HTTP timeout); `abstraction-and-its-cost` — the tidy `curl` call hides four
  protocols you must be able to peel back.

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./04-just-enough-python.md) (socket examples are
  Python).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x**; the **`curl`**, **`dig`**, and
  **`ping`** CLIs; network access to reach a real URL.
- **Assumed knowledge**: reading/writing basic Python; comfort running terminal commands. No prior
  networking background required.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: Python `socket` TCP API (`bind`/`listen`/`accept`/`connect`,
  `create_connection()`) unchanged; `curl -v` verbose format (`>` sent, `<` received, `*` info) unchanged;
  **TLS 1.3 (RFC 8446)** is current, 1-RTT handshake description accurate. `dig` output format stable but
  not primary-source re-quoted — spot-check `man dig` at authoring. (docs.python.org / ietf.org)
- 2026-07-14 — re-verified (pre-authoring `web-researcher` sweep, Phase 13): Python `socket` TCP API
  (`bind`/`listen`/`accept`/`connect`, `create_connection()`) still matches
  `docs.python.org/3/library/socket.html` (Python 3.14 docs); `curl -v` verbose format (`>` sent, `<`
  received, `*` info) unchanged; RFC 9293 (TCP) still current, not superseded; RFC 9110 (HTTP semantics)
  still current; RFC 9112 (HTTP/1.1 message syntax) still current but **updated** (not obsoleted) by
  [RFC 9931](https://www.rfc-editor.org/rfc/rfc9931) — a narrow `CONNECT`-proxy security addendum that
  doesn't change request/status-line ABNF, no correction needed; AAAA still RFC 3596; `nc -l <port>`
  positional-port syntax confirmed current on OpenBSD per
  [man.openbsd.org/nc.1](https://man.openbsd.org/nc.1); IANA ports 80/443/53/22 confirmed
  http/https/domain/ssh unchanged. **Correction**: RFC 8446 (TLS 1.3) has been obsoleted by
  [RFC 9846](https://www.rfc-editor.org/rfc/rfc9846) (E. Rescorla, published 2026, confirmed by direct
  fetch of both `rfc-editor.org/rfc/rfc8446` — "This RFC is now obsolete, see RFC 9846" — and
  `rfc-editor.org/rfc/rfc9846` itself) — a "bis" revision retaining the same TLS 1.3 version number and
  1-RTT handshake, so no worked-example content changes needed; the DD-35 TLS citation below is corrected
  accordingly. (docs.python.org / ietf.org / iana.org / man.openbsd.org)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`), re-verified 2026-07-14 (Phase 13 pre-authoring sweep). Sources: IETF
> RFCs, IANA port registry, `docs.python.org`, curl/OpenSSL/OpenBSD man pages, ISC BIND docs. All
> checkable claims verified; one correction applied 2026-07-14 (TLS RFC citation, see below).

- **Transport (co-06/07/08)** — TCP three-way handshake + "reliable, in-order, byte-stream" per
  **[RFC 9293](https://www.rfc-editor.org/rfc/rfc9293)** (W. Eddy ed., 2022, obsoletes 793 — file correctly
  cites the current RFC); UDP "delivery and duplicate protection are not guaranteed" per
  [RFC 768](https://www.rfc-editor.org/rfc/rfc768); ICMP Echo (Type 8)/Echo Reply (Type 0) per
  [RFC 792](https://www.rfc-editor.org/rfc/rfc792).
- **HTTP (co-12..18)** — request/status line ABNF + message structure per
  [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112); method semantics (GET/HEAD/POST/PUT/DELETE), status
  classes 2xx-5xx, header fields, and 3xx `Location` redirects per
  [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110). (These HTTP RFCs govern ~25 examples but aren't in
  Read more — advisory only; every claim checks out against them.)
- **TLS + ports (co-05/17)** — 1-RTT TLS 1.3 full handshake per
  [RFC 9846](https://www.rfc-editor.org/rfc/rfc9846) §2 (**corrected 2026-07-14**: RFC 8446 was obsoleted by
  RFC 9846 in 2026 — a minor, backward-compatible "bis" revision keeping the same TLS 1.3 version number
  and 1-RTT handshake, so no example content changes needed); ports 80/443/53/22 (http/https/domain/ssh)
  confirmed unchanged per the
  [IANA registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml).
- **DNS (co-04, Read more)** — A/CNAME/MX/NS/TXT per [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035)
  (Mockapetris, 1987); **AAAA is RFC 3596** (not 1035 — file does not misattribute it); `dig +trace`
  root→TLD→authoritative per [ISC BIND](https://kb.isc.org/docs/aa-00208).
- **Tooling + stdlib (co-10/19/21/23, ex-38/59)** — `socket`/`bind`/`listen`/`accept` +
  `SO_REUSEADDR` TIME_WAIT reuse + `ConnectionRefusedError` per
  [Python docs](https://docs.python.org/3/library/socket.html); `curl` `-v`/`-I`/`-L`/`-d`/`-H`/`-w`/
  `--compressed` per [curl manpage](https://curl.se/docs/manpage.html); `nc -l <port>` (positional port,
  BSD/macOS-native) per [OpenBSD nc.1](https://man.openbsd.org/nc.1); `openssl s_client -connect host:443`
  per [OpenSSL docs](https://docs.openssl.org/master/man1/openssl-s_client/).
- **Read more** — _Computer Networks_ (Tanenbaum/Feamster/Wetherall, 6th ed. 2021); _TCP/IP Illustrated
  Vol. 1_ (Fall/Stevens, 2nd ed. 2011); RFC 9293; RFC 1035; Beej's Guide to Network Programming — all
  author/edition/year/URL confirmed. `example.com` (demo host) is RFC-2606-reserved for documentation.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · client-server-model** — one side (the client) initiates a request and the other (the server)
  listens and responds; every exchange in this topic has these two roles.
- **co-02 · url-anatomy** — a URL decomposes into scheme, host, optional port, path, and query string,
  each of which routes the request.
- **co-03 · dns-resolution** — a hostname is translated to an IP address by resolvers before any
  connection can open (`name → address`).
- **co-04 · dns-record-types** — DNS holds typed records — `A`/`AAAA` (addresses), `CNAME` (alias),
  `MX` (mail), `NS` (nameservers), `TXT` — each answering a different question.
- **co-05 · ip-and-ports** — hosts are addressed by IPv4/IPv6 addresses and services by port numbers,
  with well-known ports (80/443/22/53) fixing common services.
- **co-06 · icmp-ping** — `ping` sends ICMP echo requests to test reachability and measure round-trip
  latency, independent of any application protocol.
- **co-07 · tcp-connection** — TCP establishes a connection via a three-way handshake and then delivers
  a reliable, ordered byte stream.
- **co-08 · udp-datagram** — UDP sends connectionless, unreliable, message-oriented datagrams with no
  handshake, ordering, or delivery guarantee.
- **co-09 · tcp-vs-udp** — TCP trades latency for reliability/ordering; UDP trades guarantees for
  low-overhead speed — you pick per use case.
- **co-10 · sockets-api** — the Berkeley sockets API (`socket`/`bind`/`listen`/`accept`/`connect`/
  `send`/`recv`) is the programmatic interface to TCP and UDP.
- **co-11 · request-response-framing** — a byte stream has no built-in message boundaries, so a protocol
  frames messages (e.g. newline-delimited) and reassembles partial reads.
- **co-12 · http-request-structure** — an HTTP request is a request line (method + path + version),
  headers, a blank line, and an optional body.
- **co-13 · http-response-structure** — an HTTP response is a status line (version + code + reason),
  headers, a blank line, and an optional body.
- **co-14 · http-methods** — `GET`, `POST`, `PUT`, `DELETE`, and `HEAD` carry distinct semantics for
  reading, creating, replacing, deleting, and header-only requests.
- **co-15 · http-status-codes** — status codes group into `2xx` success, `3xx` redirect, `4xx` client
  error, and `5xx` server error classes.
- **co-16 · http-headers** — headers such as `Host`, `Content-Type`, `Content-Length`, `User-Agent`, and
  `Accept-Encoding` carry request/response metadata.
- **co-17 · http-vs-https-tls** — HTTPS wraps HTTP in a TLS session (1-RTT TLS 1.3 handshake) that
  encrypts and authenticates the connection over port 443.
- **co-18 · redirects** — a `3xx` response with a `Location` header directs the client to re-request a
  new URL.
- **co-19 · curl-tooling** — `curl` drives HTTP from the terminal: `-v` (verbose), `-I` (head), `-L`
  (follow), `-d` (body), `-H` (header), `-w` (timing).
- **co-20 · dns-tooling** — `dig`, `nslookup`, and `host` query DNS directly, revealing records,
  resolvers, and the resolution path.
- **co-21 · connection-inspection** — `nc` (netcat) opens or listens on raw TCP sockets so you can send
  and read protocol bytes by hand.
- **co-22 · content-negotiation** — `Accept`/`Content-Type` headers and `Accept-Encoding: gzip` let
  client and server agree on representation and compression.
- **co-23 · stdlib-http-client** — Python's `http.client` and `urllib.request` issue HTTP(S) requests
  and expose status, headers, and body programmatically.

## Worked examples

Colocated under `networking-essentials/learning/code/`; each is a runnable CLI/socket recipe (annotated
Python plus `curl`/`dig`/`nc` transcripts, DD-20/DD-30) with a verifiable observable, and each cites the
`co-NN` it exercises. Contiguous `ex-01..ex-82`.

### Beginner

- **ex-01 · curl-a-url** — run `curl https://example.com` — verify the HTML body prints. (co-01, co-12)
- **ex-02 · curl-verbose** — run `curl -v https://example.com` — verify `>` request lines and `<`
  response lines both print. (co-19, co-13)
- **ex-03 · curl-headers-only** — run `curl -I https://example.com` — verify only the status line and
  response headers print (no body). (co-19, co-16)
- **ex-04 · read-status-line** — from `curl -v` output, locate the `HTTP/1.1 200 OK` line — verify a
  `2xx` status. (co-13, co-15)
- **ex-05 · identify-request-line** — in `curl -v`, find the `GET / HTTP/1.1` request line — verify
  method + path + version. (co-12)
- **ex-06 · inspect-response-headers** — with `curl -v`, read `Content-Type` and `Content-Length` —
  verify both appear. (co-16)
- **ex-07 · url-anatomy-breakdown** — label `https://host:443/path?q=1` as scheme/host/port/path/query —
  verify each component. (co-02)
- **ex-08 · default-ports** — compare `curl http://example.com` and `curl https://example.com` — verify
  HTTP defaults to port 80 and HTTPS to 443. (co-05, co-02)
- **ex-09 · ping-host** — run `ping -c 3 example.com` — verify three ICMP replies with round-trip times.
  (co-06)
- **ex-10 · ping-shows-ip** — read the `ping` output — verify it prints the resolved IP address. (co-06,
  co-03)
- **ex-11 · dig-a-record** — run `dig example.com A` — verify the ANSWER section shows an A-record IP.
  (co-03, co-04)
- **ex-12 · dig-short** — run `dig +short example.com` — verify only the IP address prints. (co-20,
  co-03)
- **ex-13 · dig-aaaa** — run `dig example.com AAAA` — verify an IPv6 address (or empty ANSWER) is shown.
  (co-04, co-05)
- **ex-14 · dig-mx** — run `dig example.com MX` — verify mail-exchanger records with priorities. (co-04)
- **ex-15 · dig-ns** — run `dig example.com NS` — verify the authoritative nameservers. (co-04)
- **ex-16 · dig-cname** — run `dig www.<domain> CNAME` — verify a CNAME alias resolves to its target.
  (co-04, co-03)
- **ex-17 · dig-txt** — run `dig example.com TXT` — verify TXT records print. (co-04)
- **ex-18 · nslookup-basic** — run `nslookup example.com` — verify the server and resolved address.
  (co-20, co-03)
- **ex-19 · host-command** — run `host example.com` — verify the A/AAAA/MX summary. (co-20, co-04)
- **ex-20 · dig-trace** — run `dig +trace example.com` — verify iterative resolution from the root to
  the authoritative server. (co-20, co-03)
- **ex-21 · curl-follow-redirect** — run `curl -IL http://<redirecting-host>` — verify a `3xx` then the
  final `200`. (co-18, co-19)
- **ex-22 · curl-status-404** — run `curl -o /dev/null -s -w "%{http_code}\n" <missing-path>` — verify
  it prints `404`. (co-15, co-19)
- **ex-23 · curl-user-agent** — run `curl -A "myagent" -v ...` — verify the `User-Agent: myagent`
  request header is sent. (co-16, co-19)
- **ex-24 · curl-custom-header** — run `curl -H "X-Demo: 1" -v ...` — verify the custom header appears in
  the request. (co-16, co-19)
- **ex-25 · curl-timing** — run `curl -o /dev/null -s -w "time_total=%{time_total}\n" ...` — verify a
  total-time figure prints. (co-19)
- **ex-26 · curl-head-method** — run `curl -I ...` (HEAD) — verify headers return with no body. (co-14,
  co-19)
- **ex-27 · well-known-ports** — map 80/443/22/53 to HTTP/HTTPS/SSH/DNS — verify each association.
  (co-05)
- **ex-28 · resolve-then-curl-by-ip** — `dig +short` a host, then `curl -H "Host: <name>" http://<ip>` —
  verify the same page loads by IP. (co-03, co-05, co-19)

### Intermediate

- **ex-29 · tcp-echo-server** — write `server.py` that binds/listens on a port and echoes received bytes
  — verify it starts and accepts a connection. (co-10, co-07)
- **ex-30 · tcp-echo-client** — write `client.py` that connects and sends a line — verify it receives the
  echoed line. (co-10, co-01)
- **ex-31 · socket-bind-listen-accept** — annotate the server's `bind`/`listen`/`accept` calls — verify
  `accept` blocks until a client connects. (co-10, co-07)
- **ex-32 · socket-connect-send-recv** — annotate the client's `connect`/`sendall`/`recv` calls — verify
  a full round-trip. (co-10)
- **ex-33 · line-framing** — frame messages with `\n` delimiters and read one line at a time — verify
  partial reads reassemble into whole lines. (co-11, co-07)
- **ex-34 · handle-partial-recv** — loop `recv` until the delimiter arrives — verify a large message
  arrives intact. (co-11)
- **ex-35 · multi-message-session** — send several lines on one connection — verify each gets its
  response in order. (co-11, co-07)
- **ex-36 · command-protocol** — implement `PING`→`PONG` and `TIME`→timestamp on the server — verify
  each command's reply. (co-11, co-01)
- **ex-37 · graceful-close** — close the client and detect an empty `recv` on the server — verify the
  server loop ends cleanly. (co-10, co-07)
- **ex-38 · reuseaddr-option** — set `SO_REUSEADDR` before `bind` — verify an immediate restart without
  "address already in use". (co-10)
- **ex-39 · one-client-at-a-time** — a sequential accept loop — verify a second client waits, then is
  served. (co-10, co-01)
- **ex-40 · concurrent-clients-threads** — spawn a thread per accepted socket — verify two clients are
  served simultaneously. (co-10, co-01)
- **ex-41 · raw-http-with-nc** — pipe `printf 'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n'` into
  `nc example.com 80` — verify a raw HTTP response prints. (co-21, co-12, co-13)
- **ex-42 · nc-listen-server** — run `nc -l 8080` and connect with `curl` — verify the raw request bytes
  appear in the listener. (co-21, co-12)
- **ex-43 · handcraft-http-request** — write the request line and `Host` header by hand over a socket —
  verify a `200` response returns. (co-12, co-16)
- **ex-44 · read-http-response-parts** — split a raw response into status line, headers, and body —
  verify each part is identifiable. (co-13, co-16)
- **ex-45 · http-get-method** — send a `GET` and inspect the response — verify the body is returned.
  (co-14, co-12)
- **ex-46 · http-post-form** — run `curl -d "a=1&b=2" <endpoint>` — verify the server receives the POST
  body. (co-14, co-19)
- **ex-47 · http-post-json** — run `curl -H "Content-Type: application/json" -d '{"x":1}' ...` — verify
  JSON is posted with the correct content-type. (co-14, co-16, co-22)
- **ex-48 · http-put-delete** — send `PUT` and `DELETE` via `curl -X` — verify each method reaches the
  endpoint. (co-14, co-19)
- **ex-49 · status-class-tour** — trigger a `200`, `301`, `404`, and `500` — verify each status class.
  (co-15)
- **ex-50 · content-length-header** — read `Content-Length` and compare it to the body byte size —
  verify they match. (co-16, co-13)
- **ex-51 · accept-header-negotiation** — send `Accept: application/json` — verify the server returns
  JSON. (co-22, co-16)
- **ex-52 · gzip-encoding** — run `curl --compressed -v` — verify `Accept-Encoding: gzip` is sent and a
  compressed response returns. (co-22, co-19)
- **ex-53 · chunked-transfer** — fetch a chunked response and note `Transfer-Encoding: chunked` — verify
  there is no fixed `Content-Length`. (co-13, co-16)
- **ex-54 · udp-echo-server** — write a `SOCK_DGRAM` server using `recvfrom`/`sendto` — verify it echoes
  a datagram. (co-08, co-10)
- **ex-55 · udp-echo-client** — send a datagram with `sendto` and read with `recvfrom` — verify the echo
  returns. (co-08, co-10)
- **ex-56 · udp-no-handshake** — send a UDP datagram to a closed port — verify there is no handshake and
  possibly no reply. (co-08, co-09)
- **ex-57 · tcp-vs-udp-contrast** — run the TCP and UDP echo pairs side by side — verify TCP guarantees
  ordered delivery while UDP may drop or reorder. (co-09, co-07, co-08)
- **ex-58 · measure-latency-socket** — time a TCP round-trip in Python — verify a millisecond figure
  prints. (co-07, co-10)
- **ex-59 · port-scan-connect** — attempt `connect` to an open vs a closed port — verify success vs
  `ConnectionRefusedError`. (co-05, co-10)
- **ex-60 · resolve-in-python** — call `socket.getaddrinfo`/`gethostbyname` — verify a host resolves to
  an IP in code. (co-03, co-10)

### Advanced

- **ex-61 · stdlib-http-client-get** — use Python `http.client` to `GET` a path — verify the status and
  body. (co-23, co-14)
- **ex-62 · urllib-request** — call `urllib.request.urlopen` — verify the response code and the read
  body. (co-23, co-13)
- **ex-63 · parse-status-and-headers** — read `resp.status` and `resp.getheaders()` — verify the status
  code and header list. (co-23, co-16)
- **ex-64 · https-with-tls** — `GET` an `https://` URL via `http.client.HTTPSConnection` — verify a
  TLS-encrypted `200`. (co-17, co-23)
- **ex-65 · inspect-tls-handshake** — run `curl -v https://...` and read the `* TLSv1.3` lines — verify
  the negotiated protocol/cipher. (co-17, co-19)
- **ex-66 · view-server-certificate** — run `openssl s_client -connect host:443` — verify the
  certificate chain prints. (co-17)
- **ex-67 · http-vs-https-contrast** — fetch the same host over port 80 and 443 — verify 443 is
  encrypted while 80 is plaintext (visible under `nc`). (co-17, co-21)
- **ex-68 · follow-redirect-manually** — read a `301` `Location` header, then request it — verify the
  final resource. (co-18, co-23)
- **ex-69 · minimal-http-client-from-socket** — issue a raw HTTP `GET` over a Python socket and print the
  status line — verify a real HTTP status. (co-10, co-12, co-13)
- **ex-70 · narrate-dns-tcp-http** — a script that resolves a host, opens a socket, sends a `GET`, and
  logs the DNS→TCP→HTTP path — verify each stage prints. (co-03, co-07, co-12)
- **ex-71 · keepalive-reuse-connection** — send two requests on one keep-alive socket — verify both
  responses return without reconnecting. (co-12, co-07)
- **ex-72 · handle-http-errors** — request a `404` and a `500` via the stdlib and branch on status class
  — verify each is handled. (co-15, co-23)
- **ex-73 · post-json-stdlib** — `POST` JSON with `http.client` and a `Content-Type` header — verify the
  server accepts it. (co-14, co-23, co-16)
- **ex-74 · timeout-on-connect** — set a socket timeout to an unreachable host — verify a `timeout` is
  raised. (co-10, co-07)
- **ex-75 · udp-packet-loss** — send several UDP datagrams rapidly — verify some may be dropped with no
  retransmission. (co-08, co-09)
- **ex-76 · concurrent-command-server** — extend the command server to serve multiple clients with
  threads — verify concurrent sessions. (co-10, co-11, co-01)
- **ex-77 · protocol-error-handling** — send a malformed command — verify the server replies with an
  error line rather than crashing. (co-11, co-01)
- **ex-78 · content-type-router** — a server returning JSON or plain text based on `Accept` — verify
  content negotiation both ways. (co-22, co-01)
- **ex-79 · measure-dns-vs-connect-time** — run
  `curl -o /dev/null -s -w "dns=%{time_namelookup} connect=%{time_connect}\n" ...` — verify separate DNS
  and TCP timing figures. (co-19, co-03, co-07)
- **ex-80 · trace-layers-on-failure** — force a DNS failure (bad host) and a TCP failure (closed port) —
  verify the error surfaces at the right layer. (co-03, co-07, co-09)
- **ex-81 · full-echo-command-protocol** — assemble the line-based TCP command server + client with
  `PING`/`TIME` and graceful shutdown — verify end-to-end round-trips on localhost. (co-10, co-11,
  co-01, co-07)
- **ex-82 · full-dns-to-http-explorer** — a script that `dig`-resolves a host, opens a TCP socket, issues
  an HTTP `GET`, and narrates DNS→TCP→HTTP with a UDP contrast note — verify a real status line and the
  contrast. (co-03, co-07, co-12, co-08, co-09)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a tiny TCP request/response protocol over Python `socket` (a line-based echo/command
  server + client) and a companion script that resolves a host with `dig`, opens a TCP connection, and
  narrates the DNS→TCP→HTTP path — runnable end-to-end on localhost.
- **Concepts exercised**: [ ] TCP client/server with `socket` [ ] request/response framing [ ] DNS
  resolution [ ] HTTP request read via stdlib [ ] TCP-vs-UDP contrast.
- **Ordered steps**:
  1. `.../learning/capstone/code/server.py` + `client.py` — a line-based TCP echo/command server.
     Verify `python3 server.py &` then `python3 client.py` round-trips messages.
  2. Add a small command set (e.g. `PING`→`PONG`, `TIME`→timestamp). Verify each command's response.
  3. `explore.py` — resolve a real host, open a socket, issue a minimal HTTP GET, print the status line.
     Verify it prints a real HTTP status.
- **Acceptance criteria**: server/client round-trip works; commands return correct responses; the explore
  script narrates the resolution + connection + response; a UDP variant is contrasted in prose.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Computer Networks** — Tanenbaum, Feamster, Wetherall (6th ed., 2021). Classic layered textbook, physical through application layer.
- **TCP/IP Illustrated, Volume 1: The Protocols** — Fall, Stevens (2nd ed., 2011). Definitive packet-level walkthrough of TCP/IP on the wire.

**Papers & articles**

- **RFC 9293: Transmission Control Protocol** — W. Eddy, ed. (2022). Current normative TCP spec. <https://www.rfc-editor.org/rfc/rfc9293>
- **RFC 1035: Domain Names — Implementation and Specification** — Paul Mockapetris (1987). Foundational DNS protocol spec still in force. <https://www.rfc-editor.org/rfc/rfc1035>
- **Beej's Guide to Network Programming** — Brian "Beej" Hall (ongoing, free). Enduring practitioner primer on the Berkeley sockets API. <https://beej.us/guide/bgnet/>

---

← Previous: [11 · Backend Essentials](./11-backend-essentials.md) · Next: [13 · Just Enough TypeScript](./13-just-enough-typescript.md) →
