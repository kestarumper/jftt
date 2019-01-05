#!/bin/bash
filename="$1"
python main.py "$filename" "TESTS_OUT/$(basename $filename).mr"

echo "TEST [$filename]"
/home/adrian/jftt/kompilator/maszyna_rejestrowa/maszyna-rejestrowa "TESTS_OUT/$(basename $filename).mr"