#!/bin/ksh

prog=${0##*/}
USAGE="Usage:  $prog [-t dir] [-l] files..."

lopts=""		# Default value
dir="/tmp"

while getopts t:l letter
do
    case "$letter" in
    t)	echo "Found '-t $OPTARG'";	dir="$OPTARG";;
    l)	echo "Found '-l'";		lopts="-l";;
    *)	echo >&2 "$USAGE"; exit 1;;
    esac
done
shift $(( OPTIND-1 ))
echo "lopts = '$lopts' and dir = '$dir'"
echo "After all options:  $@"
