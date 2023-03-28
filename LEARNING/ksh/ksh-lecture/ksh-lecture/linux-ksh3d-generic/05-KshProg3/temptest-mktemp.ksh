#!/bin/ksh

# List the current directory into a temporary file.  Then
# count the number of lines in the file and if less than 40,
# print the contents of the file.  Remove the file when
# finished.

prog=${0##*/}
TMP=$(mktemp -t ${prog}XXXXXXXX)
ls -l > "$TMP"

# Why am I using input redirection on the next line?
linecount=$(wc -l < "$TMP")
if (( linecount < 40 )); then
    lp < "$TMP"
fi
rm "$TMP"	# Better to use a "trap 0" instead.
