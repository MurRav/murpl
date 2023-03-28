#!/bin/ksh

# Ignore SIGHUP; script will continue to run if you log out
trap '' 1

# Use temporary filenames like those below for systems that
# don't have the mktemp(1) command.
prog=${0##*/}	# Strip leading directories from $0
LOG=/tmp/$prog.$$a
DATA=/tmp/$prog.$$b

# Remove the files and exit upon certain signals...
trap 'rm "$LOG" "$DATA" 2>/dev/null; exit' 0 2 3 15

echo "Temporary files created..." > "$LOG"

ls -l > "$DATA"
echo "About to check line count of $DATA" >> "$LOG"
if (( $(wc -l < "$DATA") < 40 )); then
    # Ignore keyboard interrupts
    trap '' 2 3
    lp < "$DATA"
fi
echo "All done." >> "$LOG"
