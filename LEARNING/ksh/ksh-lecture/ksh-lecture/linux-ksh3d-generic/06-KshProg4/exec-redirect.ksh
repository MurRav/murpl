#!/bin/ksh

# Redirect stdout and stderr to separate files while the loop
# is executing.  When the loop is done, restore the original
# locations of those data streams.

echo "1. Pre-loop... stdout"
echo "2. Pre-loop... stderr" 1>&2

exec 3>&1 4>&2			# Save existing streams
exec 1>myfile.stdout 2>myfile.stderr
for i in 1 2 3
do
    echo "3. Inside loop $i... stdout"
    echo "4. Inside loop $i... stderr" 1>&2
done
exec 1>&3 2>&4			# Restore original streams
exec 3>&- 4>&-			# Close copies

echo "5. Post-loop... stdout"
echo "6. Post-loop... stderr" 1>&2
