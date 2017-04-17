#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}
. $shrunlib
echo $(basename $0)

tmpdir=/tmp/gcov-report-test.$$.htmldir
mkdir -p $tmpdir
cd $tmpdir

ls *.gcov
run_gcov_report --htmldir=.

cd $INITD
rm -rf $tmpdir
exit 0
