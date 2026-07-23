#!/bin/sh
# ex-28: resolve first, then connect straight to the IP -- with Host set by hand
# dig +short prints just the answer IP -- head -1 keeps only the first if several come back
IP=$(dig +short example.com | head -1)
# curl connects DIRECTLY to $IP, bypassing DNS entirely on this request -- Host: still
# tells the server which site to serve, since one IP can legitimately host many domains (co-05)
curl -H "Host: example.com" "http://$IP"
