#!/bin/ksh
who | grep "^$1 " >/dev/null
if (( $? == 0 ))
then
    echo "$1 is currently logged in"
else
    echo "$1 is not currently logged in"
fi
