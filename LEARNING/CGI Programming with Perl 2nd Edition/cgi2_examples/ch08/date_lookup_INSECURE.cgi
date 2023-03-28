#!/usr/bin/perl -wT

##
WARNING

This warning is here to prevent this script from compiling since
you really should NOT be using this on a production web server.
If you want to experiment on a private web server, remove this warning
##

use strict;
use CGI;
use CGIBook::Error;

my $q = new CGI;
my @missing;

my $month = $q->param( "month" ) or push @missing, "month";
my $year  = $q->param( "year"  ) or push @missing, "year";
my $key   = quotemeta( $q->param( "key" ) ) or push @missing, "key";

if ( @missing ) {
    my $fields = join ", ", @missing;
    error( $q, "You left the following required fields blank: $fields."  );
}

local *FILE;

## This is INSECURE unless you first check the validity of $year and $month
open FILE, "/usr/local/apache/data/$year/$month" or
    error( $q, "Invalid month or year" );

print $q->header( "text/html" ),
      $q->start_html( "Results" ),
      $q->h1( "Results" ),
      $q->start_pre;

while (<FILE>) {
    print if /$key/;
}

print $q->end_pre,
      $q->end_html;
