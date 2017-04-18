#!/bin/sh -e

ver="$(./scripts/get-version.sh | cut -d' ' -f2)"
cd dist/work || exit 1

tar_file=$(realpath ../gcov-report-${ver}.txz)
tar -cJf $tar_file `find . -type f | sort`
echo "$tar_file done"

cd - >/dev/null
exit 0
