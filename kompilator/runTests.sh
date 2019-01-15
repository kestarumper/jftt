#!/bin/bash
testFolder=$1
for filename in $testFolder/*.imp; do
    ./kompilator "$filename" "TESTS_OUT/$(basename $filename).mr"
    rc=$?
    if [[ $rc != 0 ]]
    then
        exit $rc
    fi
done

for filename in TESTS_OUT/*.mr; do
    echo "TEST [$filename]"
    ./maszyna_rejestrowa/maszyna-rejestrowa "$filename"
    read
done