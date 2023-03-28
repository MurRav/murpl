#!/bin/ksh

# Show how ((...)) and [[...]] might be used in comparisons

# Put a zero prefix in front of "$1" in case it's empty.
var="0$1"
if (( $# > 1 || var >= 6 )); then
    echo "True. (More than one param or is greater than 6.)"
fi

# Double equals is only supported in ksh93.
if [[ "$state" == "Texas" && \
	( "$city" == "Dallas" || "$city" == "Houston") ]]
then
    echo "True.  (A big city in Texas!)"
fi
