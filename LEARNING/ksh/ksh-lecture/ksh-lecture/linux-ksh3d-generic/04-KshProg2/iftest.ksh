#!/bin/ksh

# Shows how output is produced by the object of the
# "if" statement...

if who | grep "^frank"; then
    echo "frank is currently logged in."
else
    echo "frank is not currently logged in."
fi
