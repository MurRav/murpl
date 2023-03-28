var="This is a test...  1...2...3"
echo "${var%...3}"      # Trim off shortest suffix
echo "${var%%.*}"       # Trim off longest suffix
echo "$var"		# Again, the value hasn't changed
