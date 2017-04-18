#!/bin/sh
shrunlib="$(dirname $0)/lib.sh"
test -s $shrunlib || {
    echo "ERR: $shrunlib lib not found"
    exit 1
}

SHRUN_DEBUG=false
. $shrunlib

check_version() {
    local ver=""
    local vfile=../../../../lib/gcovreport/version.py
    if test -s $vfile; then
        local vmajor=$(grep -E '^VMAJOR =' $vfile | cut -d'=' -f2)
        local vminor=$(grep -E '^VMINOR =' $vfile | cut -d'=' -f2)
        local vpatch=$(grep -E '^VPATCH =' $vfile | cut -d'=' -f2)
        printf "%s v%d.%d" $(basename $GCOV_REPORT) $vmajor $vminor
        if test 0 -ne $vpatch; then
            printf ".%d\n" $vpatch
        else
            printf "\n"
        fi
    else
        echo "ERR:'${vfile} file not found'"
    fi
}

mkdir -p $TMPDIR
cd $TMPDIR || exit 1

cmdv="$(run_custom_gcov_report --version)"
checkv="$(check_version)"
test "x${cmdv}" != "x${checkv}" && {
    echo "ERR versions mismatch: '${cmdv}' != '${checkv}'"
}

rm -rf $TMPDIR
exit 0
