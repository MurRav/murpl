#!/bin/ksh

# Demonstrates the question mark syntax for "read"...

read first?"Enter your first name: " junk
read last?"Enter your last name: "   junk

echo "Hello, $first $last!"
