#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}
. $shrunlib
echo $(basename $0)

tmpdir=/tmp/gcov-report-test.$$.htmldir
initdir=$(realpath ${PWD})
coverage=""

if test "x$COVCMD" != "x"; then
    coverage=${initdir}/${COVCMD}
fi

mkdir -p $tmpdir
cd $tmpdir

ls *.gcov
$coverage ${initdir}/$GCOV_REPORT --test-mode --htmldir=.

cd $initdir
rm -rf $tmpdir
exit 0
