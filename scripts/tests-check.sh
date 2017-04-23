#!/bin/sh

DIFF_CMD=${DIFF_CMD:-'diff'}
DIFF_ARGS=${DIFF_ARGS:-'-u'}
COVCMD=${COVERAGE_CMD:-''}

if test "x${COVCMD}" != "x"; then
    COVCMD="${COVCMD} --append"
fi

shrun_dir=shrun
tmpdir=tmpdir
myname=`basename $0`

checks_run=0
checks_start=`date '+%s'`
checks_fail=0

__report() {
    local checks_stop=`date '+%s'`
    local took=`expr ${checks_stop} - ${checks_start}`
    echo "       check(s) run: ${checks_run} - failed: ${checks_fail} - in ${took} second(s)"
}

__error() {
    echo "ERR: ${myname}: $@" >&2
}

__fail() {
    echo "[FAIL] $@"
    checks_fail=`expr 1 + $checks_fail`
}

__run_diff() {
    local f1=$1
    local f2=$2
    $DIFF_CMD $DIFF_ARGS $f1 $f2
    checks_run=`expr 1 + $checks_run`
}

__check_diff() {
    local dfile=$1
    if test -s ${dfile}; then
        cat $dfile
        __fail ${dfile}
        __report
        exit 9
    fi
    echo "[ OK ] ${dfile}"
    return 0
}

__shrun_exec() {
    for s in ${shrun_dir}/t???_*.sh; do
        n=`basename $s .sh`
        shrun_test=${shrun_dir}/${n}.test
        shrun_exe=${shrun_dir}/${n}.sh
        if test -x $shrun_exe; then
            COVERAGE_CMD="${COVCMD}" ./$shrun_exe >$shrun_test 2>&1
        fi
    done
}

__run_check() {
    local run_expect=$1
    local run_test=$2
    local run_diff=$3
    #~ echo "    expe: $run_expect"
    #~ echo "    test: $run_test"
    #~ echo "    diff: $run_diff"
    test -s $run_expect || {
        __fail "${run_expect}: not found"
        return
    }
    __run_diff $run_expect $run_test >$run_diff 2>$run_diff
    test -e $run_diff || {
        __fail "${run_diff}: not found"
        return
    }
    __check_diff $run_diff
}

# -- pre checks

test -d ${shrun_dir} || {
    __error "${shrun_dir} dir not found"
    exit 2
}

which $DIFF_CMD >/dev/null 2>/dev/null || {
    __error "${DIFF_CMD} command not found"
    exit 3
}

# -- run tests scripts

__shrun_exec

# -- check all diffs

run_list=${tmpdir}/run_list.$$

ls ${shrun_dir}/t???_*.sh 2>/dev/null | sed 's/\.sh//' >$run_list

sort -u ${run_list} >${run_list}.sort
mv -f ${run_list}.sort ${run_list}

for n in $(cat ${run_list}); do
    shrun_diff=${n}.diff
    shrun_test=${n}.test
    shrun_expect=${n}.expect
    if test -s $shrun_test; then
        __run_check $shrun_expect $shrun_test $shrun_diff
    else
        __fail "${shrun_test}: not found or empty"
    fi
done

__report
exit $checks_fail
