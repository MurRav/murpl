#!/bin/ksh
# This script takes one or more filenames on the command
# line and tells vi to edit them.  When you exit vi, it
# executes a chmod to add execute permission to them.

# First check to see if any filenames were provided.
if (( $# == 0 ))
then
    echo "$0: You must provide one or more filenames." 2>&1
    exit 1
fi
vi "$@"
# If no errors from vi, change the permissions.
if (( $? == 0 ))
then
    echo ":$1:$2:$3:$4:$5:"
    chmod ugo+x "$@"
fi
