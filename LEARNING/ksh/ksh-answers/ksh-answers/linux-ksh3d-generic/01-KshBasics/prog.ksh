#!/bin/ksh
echo "PID = $$, parameters are:"
echo "   [$@]"
echo "The script name is [$0], the 2nd parameter is :$2:"
echo ""
shift
shift
echo "After shifting..."
echo "PID = $$, parameters are:"
echo "   [$@]"
echo "The script name is [$0], the 2nd parameter is :$2:"
