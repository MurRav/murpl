#!/usr/bin/perl -wT

use strict;
use CGI;
use GD::Graph::pie;

use constant TITLE => "Morning Commute Time: Pie Chart";

my $q     = new CGI;
my $graph = new GD::Graph::pie( 300, 300 );
my @data  = (
    [ qw( Mon  Tue  Wed  Thu  Fri ) ],
    [      33,  24,  23,  19,  21   ],
);


$graph->set( 
    title           => TITLE,
    '3d'            => 0
);

my $gd_image = $graph->plot( \@data );

print $q->header( -type => "image/png", -expires => "-1d" );

binmode STDOUT;
print $gd_image->png;
