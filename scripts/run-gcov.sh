#!/bin/sh

GCC_CMD=${CC:-"gcc"}
GCOV_CMD=${GCOV:-"gcov"}
GCOV_ARGS=${GCOV_ARGS:-"-b -f"}

myname=`basename $0`

__error() {
    echo "ERR: ${myname}: $@" >&2
}

which $GCC_CMD >/dev/null 2>/dev/null || {
    __error "${GCC_CMD} command not found"
    exit 2
}
which $GCOV_CMD >/dev/null 2>/dev/null || {
    __error "${GCOV_CMD} command not found"
    exit 2
}

cc_version=`${CC} --version | head -n1 | cut -d')' -f'2-'`
gcov_version=`${GCOV} --version | head -n1 | cut -d')' -f'2-'`
test "x${cc_version}" != "x${gcov_version}" && {
    __error "${CC} and ${GCOV} versions mismatch"
    __error "${CC} ${cc_version}"
    __error "${GCOV} ${gcov_version}"
    exit 3
}

for src in *.c; do
    echo "run-gcov: ${GCOV_CMD} ${GCOV_ARGS} ${src}" >&2
    ${GCOV_CMD} ${GCOV_ARGS} ${src}
done

exit 0
