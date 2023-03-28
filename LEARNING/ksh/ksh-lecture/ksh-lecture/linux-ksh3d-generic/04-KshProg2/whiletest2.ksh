#!/bin/ksh

# Demonstrate using "shift" by printing a greeting
# message to all usernames given on the command line.

while (( $# != 0 ))
do
    echo "Hello, $1.  Nice day, isn't it?"
    shift
done
echo "All done!"
