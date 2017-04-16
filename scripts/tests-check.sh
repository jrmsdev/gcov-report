#!/bin/sh

DIFF_CMD=${DIFF_CMD:-'diff'}
DIFF_ARGS=${DIFF_ARGS:-'-u'}

test_dir=gcovhtml
expect_dir=expect
myname=`basename $0`
test_flist=${test_dir}/flist
expect_flist=${test_dir}/flist.expect

checks_run=0
checks_start=`date '+%s'`

__report() {
    local checks_stop=`date '+%s'`
    local took=`expr ${checks_stop} - ${checks_start}`
    echo "       check(s) run: ${checks_run} - in ${took} second(s)"
}

__error() {
    echo "ERR: ${myname}: $@" >&2
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
        echo "[FAIL] ${dfile}"
        __report
        cat $dfile
        exit 9
    fi
    echo "[ OK ] ${dfile}"
    return 0
}

__check_html_files_list() {
    (cd $test_dir && ls *.html 2>/dev/null | sort) >$test_flist
    (cd $expect_dir && ls *.html 2>/dev/null | sort) >$expect_flist
    __run_diff $expect_flist $test_flist >${test_flist}.diff 2>${test_flist}.diff
    __check_diff ${test_flist}.diff
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

for n in $(cat ${test_flist}); do
    tfile=${test_dir}/${n}
    dfile=${tfile}.diff
    efile=${expect_dir}/${n}
    __run_diff $efile $tfile >$dfile 2>$dfile
    __check_diff $dfile
done

__report
exit 0
