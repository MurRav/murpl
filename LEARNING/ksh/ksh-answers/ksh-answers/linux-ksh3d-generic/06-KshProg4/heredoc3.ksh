#!/bin/ksh
USAGE="Usage: $0 radius [radius...]"

if (( $# == 0 ))
then
    echo "$USAGE"
    exit 1
fi
while (( $# > 0 ))
do
    circle3.ksh <<-EOF
	$1
	EOF
    shift
done
