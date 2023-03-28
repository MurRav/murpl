#!/bin/ksh

# Run the fortune program if we have execute permission.

if [[ -x /usr/games/fortune ]]; then
    /usr/games/fortune -s
fi
echo "All done!"
