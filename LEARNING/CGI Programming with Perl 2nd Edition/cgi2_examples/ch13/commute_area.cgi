#!/usr/bin/perl -wT

use strict;
use CGI;
use GD::Graph::area;

use constant TITLE => "Average Commute Time: Area Chart";

my $q     = new CGI;
my $graph = new GD::Graph::area( 400, 300 );
my @data  = (
    [ qw( Mon  Tue  Wed  Thu  Fri ) ],
    [      33,  24,  23,  19,  21   ],
    [      17,  15,  19,  15,  24   ],
);


$graph->set( 
    title           => TITLE,
    x_label         => "Day",
    y_label         => "Minutes",
    long_ticks      => 1,
    y_max_value     => 40,
    y_min_value     => 0,
    y_tick_number   => 8,
    y_label_skip    => 2,
    bar_spacing     => 4,
    accent_treshold => 400,
);

$graph->set_legend( "Morning", "Evening" );
my $gd_image = $graph->plot( \@data );

print $q->header( -type => "image/png", -expires => "-1d" );

binmode STDOUT;
print $gd_image->png;
