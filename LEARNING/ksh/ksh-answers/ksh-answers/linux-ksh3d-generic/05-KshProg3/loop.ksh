#!/bin/ksh
clear
count=1
while (( count <= 10 ))
do
    echo "Process ID $$, loop count $count"
    let count=count+1
    sleep 5
done
