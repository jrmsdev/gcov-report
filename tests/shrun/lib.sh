SHRUN_DEBUG=${SHRUN_DEBUG:-'false'}
GCOV_REPORT="$(realpath ../bin/gcov-report.py)"
COVCMD="${COVERAGE_CMD}"
INITD="$(pwd)"
MYNAME="shrun/$(basename $0 .sh)"
TMPDIR=${INITD}/testdata/${MYNAME}.tmpdir

echo "$MYNAME" # ensure at least one line of output

test -x $GCOV_REPORT || {
    echo "ERR ${MYNAME}: $GCOV_REPORT script not found"
    exit 1
}

test -d ./testdata || {
    echo "ERR ${MYNAME}: testdata dir not found"
    exit 1
}

shrun_debug() {
    $SHRUN_DEBUG && echo "D: $@" >&2
}

shrun_debug "INITD: $INITD"
shrun_debug "TMPDIR: $TMPDIR"

run_gcov_report() {
    local covcmd=""
    local gcov_cmd=""
    if test "x$COVCMD" != "x"; then
        covcmd="${INITD}/$COVCMD"
        export COVERAGE_FILE=${INITD}/.coverage
    fi
    gcov_cmd="$GCOV_REPORT --test-mode  --htmldir=$TMPDIR --gcovdir=$TMPDIR $@"
    shrun_debug "RUN: $covcmd $gcov_cmd"
    $covcmd $gcov_cmd
}
