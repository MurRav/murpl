#!/bin/ksh
# This script asks the user for the type of terminal
# they are using.  This is used to set the TERM variable.

PROG=${0##*/}
USAGE="$PROG term"
LIST="ansi dumb ibm3151 ibmpc vt100 vt220"
TERM=""

# As long as there is no setting for TERM, keep looping.
while [[ "$TERM" = "" ]]
do
    echo >&2 "Enter the option number corresponding to your"
    echo >&2 "choice.  If your terminal name doesn't appear,"
    echo >&2 "enter its name from the terminfo database."
    echo >&2 "Invalid names will cause the menu to be"
    echo >&2 "displayed again."

    # Notice the two-line prompt.
    PS3="Press <Enter> to see the list again.
Enter your choice here: "

    # Notice how $LIST doesn't have double quotes around it!
    select i in $LIST
    do
        if [[ "$i" = "" ]]; then i="$REPLY"; fi
        # Test to see if it's a valid terminal name...
        tput -T "$i" clear > /dev/null 2>&1
        if (( $? == 0 || $? == 4 )); then
            TERM="$i"
            echo >&2	# To make the output look nice
            break
        else
            echo >&2 "'$i' is an invalid TERM value."
        fi
    done
done
tset "$TERM"
echo "$TERM"
