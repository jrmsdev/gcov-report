#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}

SHRUN_DEBUG=false
. $shrunlib

mkdir -p $TMPDIR || exit 1

#~ export GCOV_REPORT_DEBUG=1
run_custom_gcov_report --gcovdir=${TESTDATA}/gcovs --htmldir=${TMPDIR}

echo "HTML FILES:"
(cd ${TMPDIR} && ls *.html | sort)
echo

rm -rf $TMPDIR
exit 0
