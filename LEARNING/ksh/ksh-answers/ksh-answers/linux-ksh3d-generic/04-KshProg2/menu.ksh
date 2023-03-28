#!/bin/ksh

# Display a menu with four options.

CALC="Calculate the volume of a box"
ONSYS="Identify whether a user is logged in"
PERMS="List the access associated with a file"
EXIT="Exit"

PS3="Enter a selection (press <Enter> to redisplay menu): "

select choice in "$CALC" "$ONSYS" "$PERMS" "$EXIT"
do
    case "$choice" in
    "$CALC")	box2.ksh ;;
    "$ONSYS")	loguser4.ksh ;;
    "$PERMS")	fileperms2.ksh ;;
    "$EXIT")	exit 0 ;;
    *)		echo >&2 "'$choice' is not a valid option.";
		echo >&2 ;;
    esac
done
