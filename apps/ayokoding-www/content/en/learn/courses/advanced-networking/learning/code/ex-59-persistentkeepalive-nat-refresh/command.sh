#!/bin/sh
# ex-59: with PersistentKeepalive = 25 set and NO application traffic sent at
# all, wg show's "sent" byte counter should still tick upward every ~25s --
# proof the keepalive packets are firing on their own schedule, which is
# EXACTLY the mechanism that would keep a real NAT mapping from expiring (co-28)
wg show  # baseline, right after the tunnel comes up
sleep 32 # deliberately idle -- no ping, no other traffic sent at all
wg show  # re-check -- only automatic keepalives could have moved the counters
