#!/usr/bin/perl -wT

use strict;
use CGI;

my $q = new CGI;
print $q->header( "text/plain" );

print "These are the HTTP environment variables I received:\n\n";

foreach ( $q->http ) {
    print "$_:\n";
    print "  ", $q->http( $_ ), "\n";
}
