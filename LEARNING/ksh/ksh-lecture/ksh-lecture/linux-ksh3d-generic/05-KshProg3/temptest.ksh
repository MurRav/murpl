#!/bin/ksh

# List the current directory into a temporary file.  Then count
# the number of lines in the file and if less than 40, print
# the contents of the file.  Remove the file when finished.

prog=${0##*/}
TMP="/tmp/$prog.$$"
ls -l > "$TMP"

linecount=$(wc -l < "$TMP")
if (( linecount < 40 )); then
    lp < "$TMP"
fi
rm "$TMP"
