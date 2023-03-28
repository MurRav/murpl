prog=/usr/bin/ls
echo "1. $prog"
echo "2. ${prog##*/}"	# Remove the directory portion
echo "3. ${prog%/*}"	# Remove the base filename portion
file=MAIN.FOR
echo "4. ${file%.FOR}"	# Only remove trailing '.FOR'
echo "5. ${file%.*}"	# Remove any extension
