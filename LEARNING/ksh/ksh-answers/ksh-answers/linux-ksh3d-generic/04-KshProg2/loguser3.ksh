#!/bin/ksh
USAGE="Usage:  $0 userid [userid...]"

if (( $# < 1 ))
then
    echo "$USAGE" >&2
    exit 1
fi

for user
do
    who | grep "^$user " >/dev/null
    if (( $? == 0 ))
    then
        echo "$user is currently logged in"
    else
        echo "$user is not currently logged in"
    fi
done
