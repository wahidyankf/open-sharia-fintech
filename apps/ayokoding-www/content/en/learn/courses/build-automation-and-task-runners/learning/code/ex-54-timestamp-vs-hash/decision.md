# Timestamp versus content freshness

| Model                   | Rebuild or reuse decision                                 |
| ----------------------- | --------------------------------------------------------- |
| Make                    | output missing or prerequisite modification time is newer |
| Content-addressed build | complete declared input fingerprint matches or differs    |

An mtime is an efficient local signal; a content fingerprint can identify equivalent work across machines.
