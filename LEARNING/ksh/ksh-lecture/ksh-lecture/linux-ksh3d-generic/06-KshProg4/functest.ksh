#!/bin/ksh

prog=${0##*/}
USAGE="Usage: $prog"

# This syntax is from the Bourne shell; bugs emulated in ksh
bsh_func() {
    # This function calculates the area of a circle.
    # The result is printed to stdout so that the calling
    # shell can use command substitution to retrieve it.
    echo "scale=4; 3.1415 * $1 * $1" | bc
}

# This is the new Bash/Korn shell syntax.
# Korn shell eliminates bugs where possible and practical.
function ksh88_func {
    echo "scale=4; 3.1415 * $1 * $1" | bc
}

# This example replaces the "bc" command with the built-in
# floating point that is available in ksh93.
function ksh93_func {
    typeset -F area	# Error in some versions of ksh88
    (( area = 3.1415 * $1 * $1 ))
    echo "$area"
}

if (( $# != 0 )); then
    echo >&2 "$USAGE"
    exit 1
fi

bsh_func 3	# Prints the result on stdout
ksh88_func 4
ksh93_func 5
