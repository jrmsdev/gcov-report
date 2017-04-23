#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}

SHRUN_DEBUG=false
. $shrunlib

mkdir -p $TMPDIR
run_custom_gcov_report --test-mode --gcovdir=$TMPDIR --htmldir=$TMPDIR
rm -rf $TMPDIR
exit 0
