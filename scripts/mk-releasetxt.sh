#!/bin/sh

mkdir -p dist
printf "%s" "$(./scripts/get-version.sh)" >dist/release.txt

which git >/dev/null 2>/dev/null && {
    printf " %s" "$(git log -n1 | head -n1 | cut -d' ' -f2)" >>dist/release.txt
}

printf "\n" >>dist/release.txt
cat dist/release.txt
