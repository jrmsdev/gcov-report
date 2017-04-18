#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}
. $shrunlib
run_gcov_report noopt_arg0 noopt_arg1 | grep -vF 'gcov-report.py'
exit 0
