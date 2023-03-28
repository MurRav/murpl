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

# Constant: path to figlet
my $FIGLET = '/usr/local/bin/figlet';

my $q      = new CGI;
my $string = $q->param( "string" );

unless ( $string ) {
    error( $q, "Please enter some text to display." );
}

local *PIPE;

## This code is INSECURE...
## Do NOT use this code on a live web server!!
open PIPE, "$FIGLET \"$string\" |" or
    die "Cannot open pipe to figlet: $!";

print $q->header( "text/plain" );
print while <PIPE>;
close PIPE;
