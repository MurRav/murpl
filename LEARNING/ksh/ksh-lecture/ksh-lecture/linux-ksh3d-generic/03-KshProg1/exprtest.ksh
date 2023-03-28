#!/bin/ksh

# First, separate fields with only one space.
string=$(ls -ld "${1:-.}" | tr -s ' ')
echo "$string"

# Second, put owner's permissions into $owner
owner=$(expr "$string" : ".\(...\)")
echo "Permissions for the owner are '$owner'"

# Last, calculate the length of the permission field
len=$(expr "$string" : "[^ ]*")
echo "The length of the first field is $len characters"
