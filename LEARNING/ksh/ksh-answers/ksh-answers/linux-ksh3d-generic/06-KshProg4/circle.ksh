#!/bin/ksh

echo -n "Enter the radius: "
read radius junk

area=$(echo "scale=3; 3.14 * $radius * $radius" | bc)
echo "The area of the circle is $area."
