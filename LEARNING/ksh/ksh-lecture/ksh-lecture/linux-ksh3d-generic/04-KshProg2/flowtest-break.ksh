#!/bin/ksh

typeset -i count=5
while (( count > 0 ))
do
    echo "$count..."
    if (( count == 2 )); then break; fi
    count=count-1
done
echo "All done."
