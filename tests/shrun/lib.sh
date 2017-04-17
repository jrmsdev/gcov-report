GCOV_REPORT="$(realpath ../bin/gcov-report.py)"
COVCMD="${COVERAGE_CMD}"
INITD="$(pwd)"

echo "shrun $(basename $0)" # ensure at least one line of output

test -x $GCOV_REPORT || {
    echo "ERR: $GCOV_REPORT script not found"
    exit 1
}

test -d testdata || {
    echo "ERR: testdata dir not found"
    exit 1
}

run_gcov_report() {
    local covcmd=""
    if test "x$COVCMD" != "x"; then
        covcmd="${INITD}/$COVCMD"
    fi
    $covcmd $GCOV_REPORT --test-mode  --htmldir=testdata --gcovdir=testdata $@
}
