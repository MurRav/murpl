#!/bin/ksh

# Set the Input Field Separator so that colons are
# delimiters in the "read" statement.
IFS=:
cut -d: -f1,5,6 /etc/passwd | while read uname fname home
do
    # If the string starts with '/home/', we want this one
    if [[ "$home" == /home/* ]]; then
        mail "$uname" <<EOF
Hello $fname,

I've just begun an exciting career in Widget Building!
I make thousands of dollars a month by selling Widgets
and you can, too!  Today is $(date +%D), so you don't have
much time to respond.  Just email me at this address:
     i.want.money@flybynite.com
EOF
    fi
done
