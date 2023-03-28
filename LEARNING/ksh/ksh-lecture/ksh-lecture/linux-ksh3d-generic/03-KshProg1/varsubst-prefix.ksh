var="This is a test...  1...2...3"
echo "${var#*is}"       # Trim off shortest prefix
echo "${var##*is}"      # Trim off longest prefix
echo "$var"		# The value itself hasn't changed
