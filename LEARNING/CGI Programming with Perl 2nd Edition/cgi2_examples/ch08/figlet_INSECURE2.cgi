#!/usr/bin/perl -w

##
WARNING

This warning is here to prevent this script from compiling since
you really should NOT be using this on a production web server.
If you want to experiment on a private web server, remove this warning
##

use strict;
use CGI;
use CGIBook::Error;

my $FIGLET = '/usr/local/bin/figlet';

my $q      = new CGI;
my $string = $q->param( "string" );

unless ( $string ) {
    error( $q, "Please enter some text to display." );
}

unless ( $string =~ /^[\w .!?-]+$/ ) {
    error( $q, "You entered an invalid character. " .
               "You may only enter letters, numbers, " .
               "underscores, spaces, periods, exclamation " .
               "points, question marks, and hyphens." );
}
local *PIPE;

## This code is more secure, but still dangerous...
## Do NOT use this code on a live web server!!
open PIPE, "$FIGLET '$string' |" or
    die "Cannot open figlet: $!";

print $q->header( "text/plain" );
print while <PIPE>;
close PIPE;
