#!/bin/ksh
var=/this/is/a/longer/name

echo "${var##*/}"
echo "${var%/*}"

tmp=${var%/*}		# Temporary variable needed
echo "${tmp##*/}"
