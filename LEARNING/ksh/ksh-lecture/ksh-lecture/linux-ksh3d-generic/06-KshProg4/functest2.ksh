#!/bin/ksh

# Any command line parameter that consists entirely of
# digits is printed back to stdout; all other parameters are
# ignored.

# Demonstrates functions via some error handling code and
# a test expression.

prog=${0##*/}		# Remove directory prefix, if any
USAGE="Usage:  $prog number [number...]"

. ./funclib.ksh		# Read in the function library

if (( $# == 0 )); then
    error 1
fi

# The user provides some parameters on the command line
# and we print those that consist entirely of digits.
# Exit code is 0 unless an error occurs.
for number
do
    if [[ "$number" == -* ]]; then
    	error 2 "Invalid option: '$number'"
    fi
    if isOnlyDigits "$number"; then
    	echo "$number"
    fi
done
exit 0
