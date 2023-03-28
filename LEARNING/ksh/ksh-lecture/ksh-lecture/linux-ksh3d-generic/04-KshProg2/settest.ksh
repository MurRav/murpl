#!/bin/ksh

typeset -i total=0 count=0

# When will the following loop terminate?
while read filename junk
do
    # This sets $1, $2, $3, $4, ..., to whatever the
    # fields are that come from the "ls -ds" command.
    # Because "set" is built-in to the shell, this
    # is MUCH faster than previous examples.
    set -- $(ls -ds "$filename")
    total=total+$1
    count=count+1
done
echo "Total blocks in $count files is $total."
