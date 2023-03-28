#!/bin/ksh

for i in a b c d e
do
    if [[ "$i" == "c" ]]; then continue; fi
    echo "$i..."
done
echo "All done."
