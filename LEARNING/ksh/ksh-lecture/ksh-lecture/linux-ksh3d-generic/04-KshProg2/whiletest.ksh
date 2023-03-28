#!/bin/ksh

# First, initialize the numeric variables
typeset -i total=0 blocks=0 count=0

# When does the following loop terminate?
while read filename junk
do
    # Get the number of disk blocks used by "$filename"
    # (This awk(1) command is very slow; a later example
    # uses a faster technique.)
    blocks=$(ls -ds "$filename" | awk '{ print $1 }')
    total=total+blocks
    count=count+1
done
echo "Total blocks in $count files is $total."
