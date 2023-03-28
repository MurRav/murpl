#!/bin/ksh

# Create the prompt string that select will use.
# (Notice how a newline can be inside the double quotes.)
PS3="Press <Enter> to see the list again.
Enter your choice here: "

# Variables make the case statement easier...
WHERE="Where am I?"
LIST="List the contents of my current directory"
EMAIL="Read my email"
EXIT="Exit this session"

# Start by clearing the screen.
clear

select choice in "$WHERE" "$LIST" "$EMAIL" "$EXIT"
do
    case "$choice" in
    "$WHERE")	pwd ;;		# Where am I?
    "$LIST")	ls -la ;;	# List current directory
    "$EMAIL")	mail ;;		# Read my email
    "$EXIT")	exit 0 ;;	# Exit menu
    *)		echo >&2 "Invalid choice.  Try again." ;;
    esac
done
