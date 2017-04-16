GCOV_REPORT=../bin/gcov-report.py
COVCMD="${COVERAGE_CMD}"

test -x $GCOV_REPORT || {
    echo "ERR: $GCOV_REPORT script not found"
    exit 1
}

run_gcov_report() {
    $COVCMD $GCOV_REPORT $@
}
