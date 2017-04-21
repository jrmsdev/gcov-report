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

echo "cp -v ../../../t???_*.c.gcov ./"
cp ../../../t???_*.c.gcov ./

run_gcov_report >/dev/null

index_html=${TMPDIR}/index.html
if test -s $index_html; then
    cat $index_html | grep -F 'href'
else
    echo "${index_html}: file not found"
fi

cd $INITD
rm -rf $TMPDIR
exit 0
