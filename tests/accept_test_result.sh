#!/bin/sh

# test type
ttype=${1:?'test type?'}

# [t???]_name.ext - the part between [] is considered the "test id" (tid)
# in example: the tid for t000_main.c is t000
# BUG: tests should have the same id...
tid=${2:?'test id?'}

test_f=""
expect_f=""

if test "x$ttype" = "xshrun"; then
    test_f=$(ls shrun/${tid}_*.test 2>/dev/null | head -n1)
    expect_f=$(ls shrun/${tid}_*.expect 2>/dev/null | head -n1)
elif test "x$ttype" = "xgcovhtml"; then
    test_f=$(ls gcovhtml/${tid}_*.html 2>/dev/null | head -n1)
    expect_f=$(ls expect/${tid}_*.html 2>/dev/null | head -n1)
fi

(test "x" != "x$test_f" && test "x" != "x$expect_f") || {
    echo "test or expect file (or both were) not found"
    echo "test: '${test_f}'"
    echo "expect: '${expect_f}'"
    exit 1
}

echo "$test_f -> $expect_f"
cat $test_f >$expect_f

exit $?
