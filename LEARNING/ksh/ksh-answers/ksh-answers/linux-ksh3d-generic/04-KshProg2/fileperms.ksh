#!/bin/ksh
echo -n "Enter a filename: "
read file junk
if [[ -r "$file" ]]
then
    echo "You DO have read permission"
else
    echo "You DO NOT have read permission"
fi
if [[ -w "$file" ]]
then
    echo "You DO have write permission"
else
    echo "You DO NOT have write permission"
fi
if [[ -x "$file" ]]
then
    echo "You DO have execute permission"
else
    echo "You DO NOT have execute permission"
fi
