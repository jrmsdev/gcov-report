#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}

SHRUN_DEBUG=false
. $shrunlib

export GCOV_REPORT_DEBUG=1
run_custom_gcov_report -V --test-mode

exit 0
