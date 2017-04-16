#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}
. $shrunlib
echo "GCOV_REPORT: $GCOV_REPORT"
run_gcov_report --test-mode --version
exit 0
