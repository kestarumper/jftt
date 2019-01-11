#!/bin/bash
for filename in jftt2018-testy/*.imp; do
    python kompilator.py "$filename" "TESTS_OUT/$(basename $filename).mr"
    rc=$?
    if [[ $rc != 0 ]]
    then
        exit $rc
    fi
done

for filename in TESTS_OUT/*.mr; do
    echo "TEST [$filename]"
    /home/adrian/jftt/kompilator/maszyna_rejestrowa/maszyna-rejestrowa "$filename"
    read
done