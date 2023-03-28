#!/usr/bin/perl -wT

use strict;
use CGIBook::UserTracker;

local *FILE;
my $track = new CGIBook::UserTracker;
$track->base_path( "/store" );

my $requested_doc = $ENV{PATH_TRANSLATED};
unless ( -e $requested_doc ) {
    print "Location: /errors/not_found.html\n\n";
}

open FILE, $requested_doc or die "Failed to open $requested_doc: $!";

my $doc = do {
    local $/ = undef;
    <FILE>;
};

close FILE;

# This assumes we're only tracking HTML files:
print "Content-type: text/html\n\n";
$track->parse( $doc );
