#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}

SHRUN_DEBUG=false
. $shrunlib

mkdir -p $TMPDIR || exit 1

gcovfile=${TESTDATA}/gcovs/t002_noexec_error.c.gcov
test -s $gcovfile || {
    echo "${gcovfile} file not found"
    rm -rf $TMPDIR
    exit 1
}

cp $gcovfile $TMPDIR

run_custom_gcov_report --test-mode --gcovdir=$TMPDIR --htmldir=$TMPDIR >/dev/null

index_html=${TMPDIR}/index.html
if test -s $index_html; then
    cat $index_html | grep -E "^global status:"
else
    echo "${index_html}: file not found"
fi

rm -rf $TMPDIR
exit 0
