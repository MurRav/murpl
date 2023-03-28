#!/bin/ksh

read city?"What city are you from? " junk
case "$city" in
    [Dd]allas)               echo "Go, Cowboys!" ;;
    [Tt]ampa|[Cc]learwater)  echo "Go, Bucs!" ;;
    [Mm]iami)                echo "Go, Dolphins!" ;;
    # other NFL cities...
    *)                       echo "I like $city's team!" ;;
esac
