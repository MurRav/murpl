#!/bin/ksh

# First, we read in each individual value.
read length?"Enter the length: " junk
read width?"Enter the width: "   junk
read height?"Enter the height: " junk

# Now do the math and print the result
let 'vol=length*width*height'
echo "The volume of the box is $vol."
