#!/bin/ksh

# Shows how "read" is used in a script...

print -n "Enter your first name: "
read first junk

print -n "Enter your last name: "
read last junk

print "Hello, $first $last!"
