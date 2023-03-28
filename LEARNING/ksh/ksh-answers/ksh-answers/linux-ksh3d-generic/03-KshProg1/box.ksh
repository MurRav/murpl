#!/bin/ksh

echo -n "Enter the length: "
read length junk

echo -n "Enter the width: "
read width junk

echo -n "Enter the height: "
read height junk

let 'vol=length*width*height'
echo "The volume of the box is $vol."
