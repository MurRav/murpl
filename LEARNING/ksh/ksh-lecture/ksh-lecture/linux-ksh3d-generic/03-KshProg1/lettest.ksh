#!/bin/ksh

x=12 y=4

let 'z=x+y*2' "w = x + y*2"
(( x=x/2 ))
(( y=y+3 ))

if (( y > x )); then
    echo "y ($y) is larger than x ($x)"
fi
