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
relf=../../../../lib/gcovreport/release.txt

shrun_debug "get_version: $get_version"
shrun_debug "relf: $relf"

echo "$(${get_version}) 0123456789" >$relf
shrun_debug "$(cat $relf)"

relinfo=$(run_custom_gcov_report -V | cut -d' ' -f3)
echo "relinfo: ${relinfo}"

test "x0123456" != "x${relinfo}" && {
    echo "ERR invalid release info: '${relinfo}'"
}
rm -f $relf

rm -rf $TMPDIR
exit 0
