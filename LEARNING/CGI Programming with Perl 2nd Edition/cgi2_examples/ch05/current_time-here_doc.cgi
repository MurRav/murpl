#!/usr/bin/perl -wT

use strict;
use CGI;

my $timestamp = localtime;

print <<END_OF_MESSAGE;
Content-type: text/html

<html>
  <head>
    <title>The Time</title>
  </head>
  
  <body bgcolor="#ffffff">
    <h2>Current Time</h2>
    <hr>
    <p>The current time according to this system is: 
    <b>$timestamp</b></p>
  </body>
</html>
END_OF_MESSAGE
