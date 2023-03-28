RSYNC="--progress -SHavz -c -e ssh"
echo "1. Original value is: '$RSYNC'"
echo "2. Replacement made:  '${RSYNC/ -c/}'"

# Or the result could be put into another variable:
COPY=${RSYNC/ -c/}
echo "3. New variable:      '$COPY'"
