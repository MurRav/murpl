#!/bin/ksh

# Two integers, both "x" and "y"
typeset -i x=5 y	# 'x' initialized here

y=10			# 'y' initialized here
x=x+y
echo "There were $x oranges remaining."
