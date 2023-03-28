#!/bin/ksh
USAGE="Usage:  $0 userid"

if (( $# < 1 ))
then
    echo "$USAGE" >&2
    exit 1
fi

who | grep "^$1 " >/dev/null
if (( $? == 0 ))
then
    echo "$1 is currently logged in"
else
    echo "$1 is not currently logged in"
fi
