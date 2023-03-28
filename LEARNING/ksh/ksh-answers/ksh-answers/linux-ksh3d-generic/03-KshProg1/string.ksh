#!/bin/ksh
var=/usr/bin/awk

echo "${var##*/}"
echo "${var%/*}"

tmp=${var%/*}		# Temporary variable needed
echo "${tmp##*/}"
