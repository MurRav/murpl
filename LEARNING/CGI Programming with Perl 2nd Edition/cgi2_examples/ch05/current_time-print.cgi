#!/usr/bin/perl -wT

use strict;

my $timestamp = localtime;

print "Content-type: text/html\n\n";
print "<html>\n";
print "<head>\n";
print "<title>The Time</title>\n";
print "</head>\n";

print "<body bgcolor=\"#ffffff\">\n";
print "<h2>Current Time</h2>\n";
print "<hr>\n";
print "<p>The current time according to this system is: \n";
print "<b>$timestamp</b>\n";
print "</p>\n";
print "</body>\n";
print "</html>\n";
