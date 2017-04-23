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
run_gcov_report >/dev/null

if test -s $index_html; then
    cat ${TMPDIR}/index.html | grep -A4 -F '<footer'
    cat ${TMPDIR}/t000_main.c.html | grep -A4 -F '<footer'
else
    echo "${index_html}: file not found"
fi

rm -rf $TMPDIR
exit 0
