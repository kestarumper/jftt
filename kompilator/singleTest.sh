#!/bin/bash
filename="$1"
./kompilator "$filename" "TESTS_OUT/$(basename $filename).mr"

rc=$?
if [[ $rc != 0 ]]
then
    exit $rc
fi

echo "TEST [$filename]"
./maszyna_rejestrowa/maszyna-rejestrowa "TESTS_OUT/$(basename $filename).mr"