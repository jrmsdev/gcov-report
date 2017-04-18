#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}

SHRUN_DEBUG=false
. $shrunlib

mkdir -p $TMPDIR
run_gcov_report
rm -rf $TMPDIR
exit 0
