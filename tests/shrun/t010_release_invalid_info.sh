#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}
. $shrunlib

relf=../lib/gcovreport/release.txt
echo "INVALID 0123456789" >$relf

run_gcov_report -V

rm -f $relf
exit 0
