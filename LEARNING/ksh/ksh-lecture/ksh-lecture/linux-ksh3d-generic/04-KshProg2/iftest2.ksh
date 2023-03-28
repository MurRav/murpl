#!/bin/ksh

# Demonstrates how if-then-else-fi is used.

if [[ "$1" = "Dallas" ]]; then
    echo "Go, Cowboys!"
elif [[ "$1" = "Tampa" ]]; then
    echo "Go, Bucs!"
elif [[ "$1" = "Miami" ]]; then
    echo "Go, Dolphins!"
else
    echo "Go Home!!"
fi
