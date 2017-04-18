#!/bin/sh
tname=${1:?'tname? (without extension)'}
cp -p t000_main.sh ${tname}.sh
echo "NEW: shrun/$tname" >${tname}.expect
