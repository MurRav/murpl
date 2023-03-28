#!/bin/ksh
prog=${0##*/}
USAGE="Usage:  $prog [-adls] filenames"
opt_a=0
opt_d=0
opt_l=0
opt_s=0

while getopts adls letter
do
    case "$letter" in
    a)	opt_a=1 ;;
    d)	opt_d=1 ;;
    l)	opt_l=1 ;;
    s)	opt_s=1 ;;
    *)	echo "$USAGE" >&2; exit 1 ;;
    esac
done
shift $(( OPTIND-1 ))
echo "You selected:  A=$opt_a, D=$opt_d, L=$opt_l, S=$opt_s"
echo "After all options:  $@"
