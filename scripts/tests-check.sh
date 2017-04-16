#!/bin/sh

DIFF_CMD=${DIFF_CMD:-'diff'}
DIFF_ARGS=${DIFF_ARGS:-'-u'}

test_dir=gcovhtml
expect_dir=expect
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
        __fail ${dfile}
        __report
        cat $dfile
        exit 9
    fi
    echo "[ OK ] ${dfile}"
    return 0
}

__check_html_files_list() {
    local test_flist=${test_dir}/flist
    local expect_flist=${test_dir}/flist.expect
    (cd $test_dir && ls *.html 2>/dev/null | sort) >$test_flist
    (cd $expect_dir && ls *.html 2>/dev/null | sort) >$expect_flist
    __run_diff $expect_flist $test_flist >${test_flist}.diff 2>${test_flist}.diff
    __check_diff ${test_flist}.diff
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

test -d ${test_dir} || {
    __error "${test_dir} dir not found"
    exit 1
}
test -d ${expect_dir} || {
    __error "${expect_dir} dir not found"
    exit 2
}

which $DIFF_CMD >/dev/null 2>/dev/null || {
    __error "${DIFF_CMD} command not found"
    exit 3
}

__check_html_files_list

run_list=${test_dir}/run_list
ls *.run 2>/dev/null | sed 's/\.run//' >$run_list
ls *.shrun 2>/dev/null | sed 's/\.shrun//' >>$run_list
sort -u ${run_list} >${run_list}.sort
mv -f ${run_list}.sort ${run_list}

for n in $(cat ${run_list}); do
    run_diff=${test_dir}/${n}.c.diff
    run_test=${test_dir}/${n}.c.html
    run_expect=${expect_dir}/${n}.c.html
    shrun_diff=${n}.diff
    shrun_test=${n}.shrun
    shrun_expect=${expect_dir}/${n}.shrun
    if test -s $run_test; then
        #~ echo "RUN"
        __run_check $run_expect $run_test $run_diff
    fi
    if test -s $shrun_test; then
        #~ echo "SHRUN"
        __run_check $shrun_expect $shrun_test $shrun_diff
    fi
done

__report
exit $checks_fail
