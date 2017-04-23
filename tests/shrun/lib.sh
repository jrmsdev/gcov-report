SHRUN_DEBUG=${SHRUN_DEBUG:-'false'}
GCOV_REPORT="$(realpath ../bin/gcov-report.py)"
COVCMD="${COVERAGE_CMD}"
INITD="$(pwd)"
MYNAME="shrun/$(basename $0 .sh)"
TMPDIR=${INITD}/tmpdir/${MYNAME}
TESTDATA=${INITD}/testdata

echo "$MYNAME" # ensure at least one line of output

test -x $GCOV_REPORT || {
    echo "ERR ${MYNAME}: $GCOV_REPORT script not found"
    exit 1
}

test -d ./tmpdir || {
    echo "ERR ${MYNAME}: tmpdir dir not found"
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

run_custom_gcov_report() {
    local covcmd=""
    if test "x$COVCMD" != "x"; then
        covcmd="$COVCMD"
        export COVERAGE_FILE=${INITD}/.coverage
    fi
    shrun_debug "RUN: $covcmd $GCOV_REPORT $@"
    $covcmd $GCOV_REPORT $@
}

run_gcov_report() {
    run_custom_gcov_report --test-mode  --htmldir=$TMPDIR --gcovdir=${TESTDATA}/gcovs $@
}
