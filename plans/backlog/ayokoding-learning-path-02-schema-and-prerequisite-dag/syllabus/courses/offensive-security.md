# Offensive Security (By Example, Python + shell)

**Course ID**: `offensive-security` · **Format**: By Example · **Language**: Python + shell.

**Short summary**: Penetration testing, exploitation, attacker techniques

**Scope note**: thinking like an attacker to defend better — reconnaissance, scanning, exploitation, and
web-app attacks — taught **ethics-first and lab-local only**. Every technique is exercised **exclusively**
against deliberately vulnerable targets you own and run locally (OWASP Juice Shop, DVWA, a local vuln VM)
or your own app; **never** against systems you are not explicitly authorized to test. `†`: Python + shell
driving standard tooling (nmap, sqlmap, Burp/ZAP). Pairs with [`60-defensive-security`](./defensive-security.md)
(the blue-team counterpart) and applies [`58-it-and-application-security`](./it-and-application-security.md).

> **ETHICS + LEGAL (DD-15, hard rule)**: this topic teaches authorized security testing only. All labs
> are self-hosted, isolated, and owned by the learner. Unauthorized access to any system is illegal and
> out of scope. The topic opens with the ethics/authorization/scope-of-engagement framing and repeats the
> "authorized targets only" rule at every hands-on step.

## Why this exists · the big idea

- **The problem before the solution**: you cannot defend what you don't understand as an attacker — a
  defender who has never chained a real exploit guesses at what matters and hardens the wrong things.
- **Keep-this-if-you-forget-everything**: an attacker turns your assumptions into attack surface and needs
  only one working chain — thinking offensively (recon → exploit → write-up) tells you which weaknesses are
  actually reachable, so defense targets reality. Authorized, lab-local targets only.
- **Big ideas touched**: `layering-and-leaks` (attacks find the gap between trust boundaries),
  `correctness-vs-pragmatism` (one working exploit beats a hundred theoretical ones — reachability over
  completeness).

## Prerequisites

- **Prior topics**: [topic 58 IT / Application Security](./it-and-application-security.md) (OWASP Top 10, threat modeling, crypto),
  [topic 17 Security Essentials](./security-essentials.md) (injection, auth), and
  [topic 5 Just Enough Bash](./just-enough-bash.md) (tool driving).
- **Tools & environment**: a macOS/Linux terminal; an **isolated local lab** — deliberately vulnerable
  targets you own (OWASP Juice Shop, DVWA, a local vuln VM) on a private/host-only network; standard
  tooling (nmap, sqlmap, an intercepting proxy — ZAP/Burp) driven from Python/shell. **No** target you are
  not authorized to test.
- **Assumed knowledge**: the OWASP Top 10 + how vulns manifest (topic 58); shell + running CLI tools
  (topic 05); HTTP/requests (topic 11).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: tools (nmap, sqlmap, ZAP/Burp) are correctly left version-unpinned — their CLI
  syntax is stable across releases and a pinned number would go stale fast. Ethics/authorization framing
  (self-owned/authorized-only labs, written scope, no third-party targets) matches current OWASP/PTES
  rules-of-engagement practice, unchanged.
- 2026-07-12 — verified (GAP for plan owner): the file names OWASP Juice Shop, DVWA, nmap, sqlmap, and
  Burp/ZAP but does **not** mention Kali Linux anywhere. If Kali is wanted as the named lab OS, add it
  explicitly — it is free, Debian-derived, GPL-family, no licensing concern. Otherwise the OS-agnostic
  tool-only framing is intentional and correct as-is.

### DD-35 primary-source citations (fetched-and-read)

> Every framework name, phase count, tool flag, and standard below traces to a primary source the author
> fetched and READ. Unverifiable specifics carry `[Needs Verification]`.

- **Authorization / rules of engagement** `[Verified]` — [NIST SP 800-115](https://nvlpubs.nist.gov/NISTpubs/Legacy/SP/NISTspecialpublication800-115.pdf)
  §5.2: "Penetration testing should be performed only after careful consideration, notification, and
  planning"; "the assessment plan—or ROE [Rules of Engagement]—is developed" in the planning phase. This is
  the primary basis for the topic's authorized-only hard rule.
- **PTES — 7 phases** `[Verified]` — [Penetration Testing Execution Standard](https://pentest-standard.readthedocs.io/)
  (canonical readthedocs mirror; pentest-standard.org itself returned ECONNRESET): Pre-engagement
  Interactions, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post
  Exploitation, Reporting.
- **Cyber Kill Chain — 7 stages** `[Verified]` — [Lockheed Martin, Gaining the Advantage (PDF)](https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/cyber/Gaining_the_Advantage_Cyber_Kill_Chain.pdf):
  Reconnaissance, Weaponization, Delivery, Exploitation, Installation, Command & Control, Actions on
  Objectives. Verbatim defender principle: "Stopping adversaries at any stage breaks the chain of attack!"
- **MITRE ATT&CK — CURRENT IS v19 (15 tactics), NOT 14** `[Verified]` — [attack.mitre.org](https://attack.mitre.org/matrices/enterprise/):
  "a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations."
  **v19 (released 2026-04-28)** split the former **Defense Evasion (TA0005)** into **Stealth (TA0005)** +
  **Defense Impairment (TA0112)** → 15 tactics. Content citing "Defense Evasion / 14 tactics" is pre-v19; new
  content should use the 15-tactic model or note the historical term. Tactic = the _why_ (goal); technique =
  the _how_ (e.g. T1593 Search Open Websites/Domains).
- **OWASP Top 10:2025** `[Verified]` — [owasp.org/Top10/2025](https://owasp.org/Top10/2025/): current edition
  (supersedes 2021); A01 Broken Access Control … A03 Software Supply Chain Failures (new) … A10 Mishandling of
  Exceptional Conditions (new).
- **Nmap** `[Verified]` — [nmap.org Options Summary](https://nmap.org/book/man-briefoptions.html): "a free and
  open source utility… for network discovery, administration, and security auditing." Scan flags verbatim:
  `-sS/sT/sA` TCP SYN/Connect/ACK, `-sU` UDP, `-sV` version detection (intensity 0–9).
- **Web-attack CWEs / OWASP** `[Verified]` — [CWE-89 SQLi](https://cwe.mitre.org/data/definitions/89.html) +
  [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) ("insertion or 'injection' of a
  SQL query via the input data"); [CWE-79 XSS](https://cwe.mitre.org/data/definitions/79.html) +
  [OWASP XSS](https://owasp.org/www-community/attacks/xss/) (reflected/stored/DOM verbatim);
  [CWE-307](https://cwe.mitre.org/data/definitions/307.html) (excessive auth attempts) +
  [OWASP Credential Stuffing](https://owasp.org/www-community/attacks/Credential_stuffing) (brute-force vs
  credential-stuffing distinction verbatim); privilege escalation vertical/horizontal from the
  [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/03-Testing_for_Privilege_Escalation.html)
  (vertical = "more privileged accounts"; horizontal = "a similarly configured account").
- **sqlmap** `[Verified]` — [sqlmap.org](https://sqlmap.org/): "Open-source automation for detecting and
  exploiting SQL injection flaws"; five techniques (boolean-blind, time-blind, error-based, UNION, stacked).
- **Metasploit** `[Verified]` — [Rapid7 MSF overview](https://docs.rapid7.com/metasploit/msf-overview/): "A
  Ruby-based, modular penetration testing platform"; exploits execute against vulnerabilities, payloads are
  "the executable code deployed after successful exploitation" (Meterpreter = advanced payload).
- **Burp Proxy** `[Verified]` — [PortSwigger Burp Proxy docs](https://portswigger.net/burp/documentation/desktop/tools/proxy):
  "operates as a web proxy server between the browser and target applications… intercept, inspect, and modify
  traffic."
- **Password cracking** `[Verified]` — [hashcat.net](https://hashcat.net/hashcat/) ("World's fastest password
  cracker", MIT, 450+ hash types) + [NIST SP 800-115](https://nvlpubs.nist.gov/NISTpubs/Legacy/SP/NISTspecialpublication800-115.pdf)
  §5.1: dictionary/hybrid/brute-force/rainbow-table definitions verbatim; "Salting… decreases the likelihood
  of identical passwords returning the same hash." John the Ripper's own flags `[Needs Verification]`
  (openwall.com/john not independently fetched).
- **Buffer overflow** `[Verified]` — [CWE-787 Out-of-bounds Write](https://cwe.mitre.org/data/definitions/787.html)
  ("writes data past the end, or before the beginning, of the intended buffer") + NIST SP 800-115 §5.2.1.
- **Network / MITM** `[Verified]` — [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/ChapterIntroduction.html)
  ("a network packet analyzer… neither an intrusion detection system nor does it actively manipulate network
  traffic") + [RFC 826 ARP](https://datatracker.ietf.org/doc/html/rfc826) (the protocol ARP-spoofing abuses).
  ARP-spoofing-as-attack-technique verbatim primary `[Needs Verification]` (MITRE ATT&CK T1557 not fetched).
- **CVSS / CVE / NVD / Exploit-DB** `[Verified]` — [FIRST CVSS](https://www.first.org/cvss/) (current **v4.0**;
  v3.1 Base/Temporal/Environmental still dominant) + [NVD CVE process](https://nvd.nist.gov/general/cve-process)
  (CVE = "a dictionary or glossary of vulnerabilities… for specific code bases") +
  [Exploit-DB About](https://exploit-db.com/about-exploit-db) ("a CVE compliant archive of public exploits").
  Direct cve.org verbatim quote `[Needs Verification]` (JS-render issue on fetch; NVD is the substitute).
- **Social engineering / disclosure** `[Needs Verification]` — CISA (avoiding-phishing, CVD program) and
  ISO/IEC 29147 all returned HTTP 403 to direct fetch; the social-engineering and responsible-disclosure
  framing rests on search-summarized snippets, not a fetched-and-read primary. Teach conceptually; flag any
  verbatim CISA/ISO quote until a browser-based fetch confirms it.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. Every technique is authorized, lab-local only. -->

- **co-01 · ethics-authorization-scope** — every technique runs only against authorized, self-owned targets under a written scope (NIST SP 800-115 ROE).
- **co-02 · rules-of-engagement** — the rules-of-engagement document (scope, boundaries, authorization) precedes any testing.
- **co-03 · responsible-disclosure** — coordinated vulnerability disclosure and bug-bounty norms hand findings to the vendor first.
- **co-04 · attack-lifecycle** — the phased flow: reconnaissance → scanning/enumeration → exploitation → post-exploitation.
- **co-05 · ptes-phases** — the seven PTES phases structure a professional engagement.
- **co-06 · cyber-kill-chain** — Lockheed Martin's seven-stage kill chain; breaking any one stage stops the attack.
- **co-07 · mitre-attack** — the ATT&CK knowledge base distinguishes tactics (the why) from techniques (the how).
- **co-08 · reconnaissance-passive-active** — passive recon makes no target contact; active recon touches the target directly.
- **co-09 · osint** — open-source intelligence gathering from public sources only.
- **co-10 · network-scanning-nmap** — host/port/service discovery with nmap against the lab.
- **co-11 · port-scan-types** — SYN (`-sS`) vs connect (`-sT`) vs UDP (`-sU`) scan types.
- **co-12 · service-version-detection** — nmap `-sV` probing to fingerprint service versions.
- **co-13 · enumeration** — deeper enumeration (banners, directories, endpoints) after discovery.
- **co-14 · web-app-attacks** — the OWASP-class web attack surface the lab app exposes.
- **co-15 · sql-injection-exploit** — exploiting SQL injection with sqlmap and a manual proof (CWE-89).
- **co-16 · xss-exploit** — exploiting reflected/stored/DOM XSS on the lab (CWE-79).
- **co-17 · broken-auth-attacks** — brute force, credential stuffing, and password spraying against weak auth (CWE-307).
- **co-18 · broken-access-control-exploit** — IDOR and vertical/horizontal privilege escalation on the lab.
- **co-19 · intercepting-proxy** — Burp/ZAP intercepts, inspects, and modifies lab requests.
- **co-20 · request-tampering** — modifying an in-flight request to bypass client-side controls.
- **co-21 · exploitation-frameworks** — Metasploit's modular exploit/payload/module structure.
- **co-22 · payloads-shells** — reverse vs bind shells and Meterpreter as post-exploitation payloads.
- **co-23 · privilege-escalation** — local privilege escalation after gaining a foothold.
- **co-24 · password-cracking** — hashcat/John, dictionary vs brute-force vs rainbow tables, and how salting defeats them.
- **co-25 · buffer-overflow** — memory-corruption basics: an out-of-bounds write hijacking execution (CWE-787).
- **co-26 · network-attacks-mitm** — ARP spoofing, man-in-the-middle, and packet capture with Wireshark.
- **co-27 · social-engineering-phishing** — the human-layer attack surface (studied for defense).
- **co-28 · cve-exploit-db** — vulnerability databases (NVD, Exploit-DB) to find public exploits for a version.
- **co-29 · cvss-severity** — rating a finding's severity with a CVSS score/vector.
- **co-30 · finding-report** — a professional finding write-up: reproduction + impact + remediation.
- **co-31 · lab-isolation** — an isolated, host-only, self-hosted lab so nothing can reach external systems.

## Worked examples

Colocated under `offensive-security/learning/`; Python + shell driving tooling against the local lab only
(DD-20/DD-30). **Every example header restates "authorized lab target only".** Contiguous `ex-01..ex-78`.
Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · ethics-authorization** — annotate a rules-of-engagement + authorization statement — verify scope + authorized-target-only. (co-01)
- **ex-02 · scope-boundaries** — annotate in-scope vs out-of-scope targets — verify out-of-scope is explicit. (co-01, co-02)
- **ex-03 · roe-document** — draft a rules-of-engagement document for the lab — verify it precedes testing. (co-02)
- **ex-04 · responsible-disclosure** — annotate a coordinated-disclosure timeline — verify the vendor-first flow. (co-03)
- **ex-05 · lab-isolation-setup** — annotate a host-only isolated lab network — verify no route to external systems. (co-31)
- **ex-06 · lab-target-juiceshop** — stand up OWASP Juice Shop locally — verify it responds on localhost. (co-31)
- **ex-07 · attack-lifecycle-phases** — annotate recon→scan→exploit→post-exploit phases — verify all four appear. (co-04)
- **ex-08 · ptes-phases** — annotate the seven PTES phases — verify all seven are named. (co-05)
- **ex-09 · cyber-kill-chain** — annotate the Lockheed Martin seven-stage kill chain — verify all seven stages. (co-06)
- **ex-10 · killchain-break** — annotate breaking the chain at one stage — verify the defender principle. (co-06)
- **ex-11 · mitre-attack-tactic-technique** — annotate an ATT&CK tactic vs technique — verify the why-vs-how distinction. (co-07)
- **ex-12 · attack-reconnaissance-tactic** — annotate the Reconnaissance tactic (TA0043) — verify its goal. (co-07, co-08)
- **ex-13 · passive-recon** — annotate passive reconnaissance (no target contact) — verify no packets are sent. (co-08)
- **ex-14 · active-recon** — annotate active reconnaissance against the lab — verify direct contact. (co-08)
- **ex-15 · osint-gather** — gather OSINT on a self-owned lab target — verify only public sources are used. (co-09)
- **ex-16 · nmap-host-discovery** — an nmap host-discovery sweep of the lab subnet — verify live hosts found. (co-10)
- **ex-17 · nmap-port-scan** — an nmap port scan of the lab host — verify open ports listed. (co-10, co-11)
- **ex-18 · nmap-syn-scan** — annotate a SYN scan (`-sS`) vs connect scan (`-sT`) — verify the difference. (co-11)
- **ex-19 · nmap-udp-scan** — an nmap UDP scan (`-sU`) of the lab — verify UDP services. (co-11)
- **ex-20 · nmap-version-detect** — nmap service/version detection (`-sV`) — verify service versions. (co-12)
- **ex-21 · nmap-parse-python** — parse nmap output in Python — verify structured host/port data. (co-10)
- **ex-22 · service-enumeration** — enumerate a discovered service (banner/endpoints) — verify enumerated detail. (co-13)
- **ex-23 · directory-enum** — enumerate web directories on the lab app — verify discovered paths. (co-13)
- **ex-24 · attack-surface-map** — map the lab app's attack surface from recon — verify inputs catalogued. (co-13, co-14)
- **ex-25 · web-attack-classes** — annotate the OWASP-class web attack surface — verify the categories. (co-14)
- **ex-26 · http-request-python** — send a crafted HTTP request to the lab in Python — verify the response captured. (co-14)

### Intermediate

- **ex-27 · sqli-manual** — a manual SQL-injection proof against DVWA — verify the injected clause returns data. (co-15)
- **ex-28 · sqli-sqlmap** — sqlmap detecting a SQLi point on the lab — verify the vulnerable parameter. (co-15)
- **ex-29 · sqli-dump** — sqlmap dumping a lab table — verify extracted rows (lab data only). (co-15)
- **ex-30 · sqli-blind** — annotate boolean/time-blind SQLi — verify the inference technique. (co-15)
- **ex-31 · xss-reflected-exploit** — trigger a reflected XSS on the lab — verify script execution. (co-16)
- **ex-32 · xss-stored-exploit** — plant a stored XSS on the lab — verify persistence. (co-16)
- **ex-33 · xss-payload** — craft an XSS payload in Python — verify it fires in the lab. (co-16)
- **ex-34 · brute-force-login** — a dictionary brute-force against a lab login — verify a hit. (co-17)
- **ex-35 · credential-stuffing** — annotate credential stuffing vs brute force — verify the distinction. (co-17)
- **ex-36 · password-spraying** — annotate password spraying (one password, many accounts) — verify the pattern. (co-17)
- **ex-37 · rate-limit-bypass** — annotate why missing rate limits enable brute force (CWE-307) — verify the gap. (co-17)
- **ex-38 · idor-exploit** — exploit an IDOR on the lab (access another user's record) — verify unauthorized access. (co-18)
- **ex-39 · vertical-privesc-web** — exploit vertical privilege escalation on the lab — verify admin access. (co-18)
- **ex-40 · horizontal-privesc-web** — exploit horizontal privilege escalation — verify same-tier data access. (co-18)
- **ex-41 · proxy-intercept** — intercept a lab request with ZAP/Burp — verify the request is captured. (co-19)
- **ex-42 · proxy-inspect** — inspect a lab request/response in the proxy — verify headers/body visible. (co-19)
- **ex-43 · request-tamper** — tamper an in-flight lab request via the proxy — verify the modified value takes effect. (co-20)
- **ex-44 · proxy-repeater** — replay a modified request with the proxy repeater — verify the altered response. (co-20)
- **ex-45 · metasploit-module** — annotate a Metasploit exploit module's structure — verify exploit/payload/options. (co-21)
- **ex-46 · metasploit-exploit-lab** — run a Metasploit exploit against the lab VM — verify a session opens. (co-21)
- **ex-47 · payload-reverse-shell** — annotate a reverse vs bind shell payload — verify who connects to whom. (co-22)
- **ex-48 · meterpreter-session** — annotate a Meterpreter post-exploitation session — verify the capabilities. (co-22)
- **ex-49 · privesc-local** — annotate a local privilege-escalation path on the lab host — verify the escalation. (co-23)
- **ex-50 · privesc-enum** — enumerate privesc opportunities on the lab host — verify misconfigs found. (co-23)
- **ex-51 · hash-capture** — capture a password hash on the lab — verify the hash format. (co-24)
- **ex-52 · hashcat-dictionary** — crack a lab hash with a dictionary attack — verify the recovered password. (co-24)
- **ex-53 · brute-vs-dictionary** — annotate brute-force vs dictionary vs rainbow-table cracking — verify the trade-off. (co-24)
- **ex-54 · salt-defeats-rainbow** — annotate why salting defeats rainbow tables — verify the effect. (co-24)

### Advanced

- **ex-55 · buffer-overflow-anatomy** — annotate an out-of-bounds write (CWE-787) — verify the overwritten memory. (co-25)
- **ex-56 · overflow-controlled** — annotate controlling execution via an overflow (lab binary) — verify instruction-pointer control. (co-25)
- **ex-57 · packet-capture** — capture lab traffic with Wireshark — verify packets displayed. (co-26)
- **ex-58 · arp-spoof** — annotate an ARP-spoofing MITM on the lab network — verify the poisoned mapping. (co-26)
- **ex-59 · mitm-intercept** — annotate intercepting lab traffic via MITM — verify captured plaintext. (co-26)
- **ex-60 · phishing-annotate** — annotate a phishing lure (defensive framing) — verify the social-engineering vector. (co-27)
- **ex-61 · social-eng-pretext** — annotate a pretexting scenario — verify the human-layer manipulation. (co-27)
- **ex-62 · cve-lookup** — look up a CVE in the NVD for a lab-installed version — verify the affected component. (co-28)
- **ex-63 · exploit-db-search** — find a public exploit in Exploit-DB for the lab target — verify the matching exploit. (co-28)
- **ex-64 · cve-to-exploit** — map a lab CVE to a working exploit — verify the version match. (co-28)
- **ex-65 · cvss-rate** — rate a lab finding with a CVSS Base score — verify the metric group. (co-29)
- **ex-66 · cvss-vector** — annotate a CVSS vector string — verify the parsed metrics. (co-29)
- **ex-67 · finding-reproduction** — write reproduction steps for a lab finding — verify they reproduce. (co-30)
- **ex-68 · finding-impact** — write the impact of a lab finding — verify it ties to a concrete risk. (co-30)
- **ex-69 · finding-remediation** — write remediation for a lab finding — verify a concrete fix. (co-30)
- **ex-70 · finding-report-full** — assemble a full finding (repro + impact + severity + remediation) — verify all parts. (co-29, co-30)
- **ex-71 · attack-chain** — chain two vulns into a single attack path on the lab — verify the chained access. (co-04, co-18)
- **ex-72 · killchain-map-engagement** — map a lab engagement onto the kill chain — verify each stage present. (co-06)
- **ex-73 · attack-map-mitre** — map lab techniques onto MITRE ATT&CK IDs — verify the technique IDs. (co-07)
- **ex-74 · post-exploit-loot** — annotate post-exploitation actions on the lab (loot/persistence) — verify confined to the lab. (co-04, co-23)
- **ex-75 · scope-reconfirm** — re-confirm authorization before each exploit — verify the authorized-only gate. (co-01)
- **ex-76 · disclosure-writeup** — draft a responsible-disclosure report for the lab finding — verify vendor-first framing. (co-03)
- **ex-77 · engagement-cleanup** — annotate cleaning up lab artifacts post-test — verify the target is restored. (co-04)
- **ex-78 · pentest-capstone** — a full authorized lab pentest: recon + two exploits + report — verify each part present + lab-only. (co-01, co-10, co-15, co-18, co-30)

## Tensions & trade-offs — when NOT to reach for this

- **Offense informs but doesn't equal defense**: a pentest proves a vuln is reachable but is a point-in-time
  snapshot. Treating a passed pentest as "secure" is the classic mistake — absence of _found_ bugs is not
  absence of bugs.
- **Tooling vs understanding**: sqlmap/Metasploit make exploitation push-button, which teaches the button,
  not the mechanism. Leaning on tools without understanding the underlying flaw produces a script-runner who
  can't adapt the attack or explain the fix.
- **When NOT (hard boundary, not a trade-off)**: offensive technique is exercised _only_ against authorized,
  self-owned, isolated targets. This "when not" is a legal and ethical absolute — unauthorized testing is a
  crime regardless of intent.

## Lineage — why it beat the alternative

- Offensive security professionalized from the recognition that defenders who never attack build imaginary
  threat models. Penetration testing, red-teaming, and responsible-disclosure norms (CERT, then bug bounties
  from ~2010) turned adversarial skill into a sanctioned discipline with rules of engagement — precisely so
  the attacker's reachability-first mindset could improve defense _legally_. The output — reproducible
  findings with impact and remediation — is the bridge that hands work to the blue team in
  [`60-defensive-security`](./defensive-security.md); the vulnerability classes themselves come from
  [`58-it-and-application-security`](./it-and-application-security.md).

## Capstone materials

Colocated under `offensive-security/learning/`; Python + shell driving tooling against the local lab only
(DD-20/DD-30). Every example header restates "authorized lab target only".

- **beginner** — a scoped nmap scan of the local lab host: discover services + versions; interpret the
  output.
- **intermediate** — exploit a SQL-injection point in DVWA/Juice Shop (sqlmap + a manual proof); document
  the finding.
- **advanced** — chain a web-app attack (e.g. broken access control → data exposure) through an intercepting
  proxy; write it up with reproduction + impact + remediation.

## Capstone spec — intra-topic (subject → full runnable, lab-local)

- **Goal**: run a small, fully-authorized penetration test against your own local vulnerable lab
  (Juice Shop/DVWA) end to end — recon/scan, enumerate, exploit at least two distinct OWASP-class
  vulnerabilities, and produce a professional finding report (reproduction, impact, CVSS-style rating,
  remediation) — establishing the attacker's view that the defensive topic then detects.
- **Concepts exercised**: [ ] rules-of-engagement + authorization scope stated up front (co-01, co-02)
  [ ] recon + scan (nmap) (co-08, co-10) [ ] enumeration (co-13) [ ] two distinct exploited vulns (e.g. SQLi
  - broken access control) (co-15, co-18) [ ] proxy-driven request tampering (co-19, co-20) [ ] a finding
    report with reproduction + impact + remediation (co-29, co-30).
- **Ordered steps**:
  1. `.../learning/capstone/rules-of-engagement.md` — scope + authorization (self-owned lab) + targets +
     boundaries. Verify only self-hosted lab targets are listed and out-of-scope is explicit.
  2. `.../learning/capstone/recon.sh` — a scoped nmap scan + service enumeration of the lab host. Verify
     discovered services match the known lab and output is captured.
  3. `.../learning/capstone/exploit/` — exploit two distinct vulns (Python/sqlmap/proxy) with a captured
     proof each. Verify each exploit reproduces and is confined to the lab.
  4. `.../learning/capstone/report.md` — per finding: reproduction + impact + severity + remediation.
     Verify each finding is reproducible from the steps and pairs a concrete remediation.
- **Acceptance criteria**: authorization/scope is stated first; recon + two exploits reproduce against the
  self-owned lab only; each finding has reproduction + impact + remediation; nothing touches an unauthorized
  system.
- **Done bar**: runnable end-to-end against the local lab + web-verified + ethics framing present at every
  hands-on step.

## Read more

**Books**

- **Penetration Testing: A Hands-On Introduction to Hacking** — Georgia Weidman (2014). Widely used, beginner-accessible introduction to offensive security methodology and tooling.
- **Metasploit: The Penetration Tester's Guide** — David Kennedy, Jim O'Gorman, Devon Kearns, Mati Aharoni (2011). The canonical guide to the most widely used open-source exploitation framework.
- **The Hacker Playbook 3: Practical Guide to Penetration Testing** — Peter Kim (2018). Popular, practically oriented red-team methodology reference.

**Papers & articles**

- **MITRE ATT&CK** — MITRE Corporation (ongoing). The industry-standard knowledge base of adversary tactics and techniques used to structure red-team engagements. <https://attack.mitre.org/>
- **OWASP Web Security Testing Guide (WSTG)** — OWASP Foundation (ongoing). The de facto standard methodology reference for web application penetration testing. <https://owasp.org/www-project-web-security-testing-guide/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Security suite — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Security suite — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 13 · Security suite.

> _Content originated in the now-closed FS-SE plan (topic 59); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
