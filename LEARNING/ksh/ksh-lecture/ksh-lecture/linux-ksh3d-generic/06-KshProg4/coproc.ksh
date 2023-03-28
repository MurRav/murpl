#!/bin/ksh

bc |&
while read expr?"Enter an expression: "
do
    # Special check for an empty string -- why?
    if [[ "$expr" != "" ]]; then
	print -p "$expr"
	read -p result
	print "The result is:  $result"
    fi
done
