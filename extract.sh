#!/bin/bash
for n in {0..9}; do
    grep "($n)" g.log | grep -v ETH | cut -d' ' -f2 >$n.prv
    grep "($n)" g.log | grep    ETH | cut -d' ' -f2 >$n.pub
done
