#!/bin/ksh

# Acts as a repository or "library" of Korn shell functions.
# Include this file using the "." (dot) command and then
# invoke the functions as needed.

# Produces a consistent look for error messages.
# Requires:  global "USAGE" and "prog" variables
# Syntax:    error <exitcode> [detail_message]
function error {
    result="$1"
    shift
    for msg
    do
    	echo >&2 "$prog: $msg"
    done
    echo >&2 "$USAGE"
    exit "$result"
}

# Returns true if the parameter contains only digits.
# Requires:  -
# Syntax:    isOnlyDigits <value>
function isOnlyDigits {
    # Note the use of the extended wildcard:
    #   "one or more digits".
    # Could also use a regular expression (ksh93 only):
    if [[ "$1" =~ ^[0-9]+$ ]]; then
    #  [[ "$1" == +([0-9]) ]]; then
	return 0
    else
	return 1
    fi
}
