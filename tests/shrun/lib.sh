GCOV_REPORT="$(realpath ../bin/gcov-report.py)"
COVCMD="${COVERAGE_CMD}"
INITD="$(pwd)"

test -x $GCOV_REPORT || {
    echo "ERR: $GCOV_REPORT script not found"
    exit 1
}

run_gcov_report() {
    local covcmd=""
    if test "x$COVCMD" != "x"; then
        covcmd="${INITD}/$COVCMD"
    fi
    $covcmd $GCOV_REPORT --test-mode $@
}
