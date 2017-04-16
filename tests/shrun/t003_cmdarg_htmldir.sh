#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}
. $shrunlib
run_gcov_report --test-mode --htmldir="fakedir"
run_gcov_report --test-mode --htmldir=
exit 0
