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
run_custom_gcov_report --test-mode --gcovdir=${TESTDATA}/gcovs --htmldir=${TMPDIR} >/dev/null

echo "HTML DOCS:"
(cd ${TMPDIR} && ls *.html)
echo

index_html=${TMPDIR}/index.html
if test -s $index_html; then
    cat $index_html | grep -F 't003_relpath.c'
else
    echo "${index_html}: file not found"
fi

rm -rf $TMPDIR
exit 0
