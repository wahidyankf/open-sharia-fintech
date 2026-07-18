#!/bin/sh
# ex-30: this reuses Example 1's exact command -- same curl -v transcript --
# examining the "* SSL connection using TLSv1.3 ..." line instead of the
# DNS/TCP/HTTP stages Example 1 focused on (co-14)
curl -s -v --http1.1 https://example.com
