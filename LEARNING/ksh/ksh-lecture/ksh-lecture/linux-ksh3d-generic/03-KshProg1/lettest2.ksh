#!/bin/ksh

x=12.2 y=4.6

let 'z=x+y*2'
let 'w=(z-x)/y'

# Note the syntax here:
if let 'z>w'; then
    echo "z ($z) is larger than w ($w)"
fi
