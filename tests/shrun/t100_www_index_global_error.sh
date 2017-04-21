#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}

SHRUN_DEBUG=false
. $shrunlib

mkdir -p $TMPDIR || exit 1
cd $TMPDIR || exit 1

gcovfile=../../../t002_noexec_error.c.gcov
test -s $gcovfile || {
    echo "${gcovfile} file not found"
    cd $INITD
    rm -rf $TMPDIR
    exit 1
}

echo "cp $gcovfile ./"
cp $gcovfile ./

run_gcov_report >/dev/null

index_html=${TMPDIR}/index.html
if test -s $index_html; then
    cat $index_html | grep -E "^global status:"
else
    echo "${index_html}: file not found"
fi

cd $INITD
rm -rf $TMPDIR
exit 0
