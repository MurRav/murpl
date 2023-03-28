#!/bin/ksh

# "reply" is lowercase, left-justified, 1 character.
# (Bug in some versions of ksh: must be "-lL1", not "-L1l")
typeset -l -L1 reply=Yes

echo "The value of 'reply' is '$reply'."
