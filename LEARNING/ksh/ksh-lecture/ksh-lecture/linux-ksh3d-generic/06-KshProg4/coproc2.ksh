#!/bin/ksh

# A silly example of reading the output of the cat(1)
# command and printing that data to the stdin of bc(1),
# then subsequently reading bc's output and displaying it.

bc |&
exec 3<&p 4>&p		# fd3 from "bc", fd4 to "bc"

cat bcfile |&
exec 5<&p 6>&p		# fd5 from "cat", fd6 to "cat"

while read -u5 expr	# Redirect from fd5 get one line
do
    # Sanity check.  If expression is empty, don't send to
    # coprocess or we'll sit waiting for a reply and there
    # won't be one!  Similarly, lines containing an equals
    # sign shouldn't wait for a reply.
    if [[ "$expr" != "" ]]; then
	print -u4 "$expr"	# "-u4" means "use fd4"
	if [[ "$expr" != *=* ]]; then
	    read -u3 result	# "-u3" means "use fd3"
	    print "The result is:  $result"
	fi
    fi
done
