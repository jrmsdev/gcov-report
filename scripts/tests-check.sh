#!/bin/sh

DIFF_CMD=${DIFF_CMD:-'diff'}
DIFF_ARGS=${DIFF_ARGS:-'-u'}

test_dir=gcovhtml
expect_dir=expect/gcovhtml
myname=`basename $0`
test_list=${test_dir}/flist
expect_list=${test_dir}/flist.expect

checks_run=0
checks_start=`date '+%s'`

__report() {
    local checks_stop=`date '+%s'`
    local took=`expr ${checks_stop} - ${checks_start}`
    echo "       check(s) run: ${checks_run} - in ${took} second(s)"
}

__abort() {
    echo "[FAIL] $@"
    __report
    exit 9
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
        __abort "[FAIL] ${dfile}"
    fi
    echo "[ OK ] ${dfile}"
    return 0
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

(cd $test_dir && ls *.html 2>/dev/null | sort) >$test_list
(cd $expect_dir && ls *.html 2>/dev/null | sort) >$expect_list

__run_diff $expect_list $test_list >${test_list}.diff 2>${test_list}.diff
__check_diff ${test_list}.diff

for n in $(cat ${test_list}); do
    tfile=${test_dir}/${n}
    dfile=${tfile}.diff
    efile=${expect_dir}/${n}
    __run_diff $efile $tfile >$dfile 2>$dfile
    __check_diff $dfile
done

__report
exit 0
