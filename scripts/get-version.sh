#!/bin/sh
SRCDIR=$(dirname $(realpath $0))/..
GCOV_REPORT=${SRCDIR}/bin/gcov-report.py

__get_version() {
    local ver=""
    local vfile=${SRCDIR}/lib/gcovreport/version.py
    if test -s $vfile; then
        vmajor=$(grep -E '^VMAJOR =' $vfile | cut -d'=' -f2)
        vminor=$(grep -E '^VMINOR =' $vfile | cut -d'=' -f2)
        vpatch=$(grep -E '^VPATCH =' $vfile | cut -d'=' -f2)
        printf "%s v%d.%d" $(basename $GCOV_REPORT) $vmajor $vminor
        if test 0 -ne $vpatch; then
            printf ".%d\n" $vpatch
        else
            printf "\n"
        fi
        return 0
    else
        echo "ERR:'${vfile} file not found'"
        return 1
    fi
}
__get_version
