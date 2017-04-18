#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}

SHRUN_DEBUG=false
. $shrunlib

mkdir -p $TMPDIR
cd $TMPDIR || exit 1

get_version=../../../../scripts/get-version.sh
cmdv="$(run_custom_gcov_report --version)"
checkv="$(${get_version})"
test "x${cmdv}" != "x${checkv}" && {
    echo "ERR versions mismatch: '${cmdv}' != '${checkv}'"
}

rm -rf $TMPDIR
exit 0
