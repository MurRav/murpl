#!/usr/bin/perl -wT

use strict;
use CGI;
use CGI::Carp qw( fatalsToBrowser );
use GD::Graph::pie;
use Image::Magick;
use POSIX qw( tmpnam );
use Fcntl;

use constant TITLE => "Morning Commute Time: Pie Chart";

my $q     = new CGI;
my $graph = new GD::Graph::pie( 300, 300 );
my @data  = (
    [ qw( Mon  Tue  Wed  Thu  Fri ) ],
    [      33,  24,  23,  19,  21   ],
    [      17,  15,  19,  15,  24   ],
);


$graph->set( 
    title           => TITLE,
    '3d'            => 0
);

my $gd_image = $graph->plot( \@data );
undef $graph;

if ( grep $_ eq "image/png", $q->Accept ) {
    print $q->header( -type => "image/png", -expires => "now" );
    binmode STDOUT;
    print $gd_image->png;
}
else {
    print $q->header( -type => "image/jpeg", -expires => "now" );
    binmode STDOUT;
    print_png2jpeg( $gd_image->png );
}

# Takes PNG data, converts it to JPEG, and prints it
sub print_png2jpeg {
    my $png_data = shift;
    my( $tmp_name, $status );
    
    # Create temp file and write PNG to it
    do {
        $tmp_name = tmpnam();
    } until sysopen TMPFILE, $tmp_name, O_RDWR | O_CREAT | O_EXCL;
    END { unlink $tmp_name or die "Cannot remove $tmp_name: $!"; }
    
    binmode TMPFILE;
    print TMPFILE $png_data;
    seek TMPFILE, 0, 0;
    close TMPFILE;
    undef $png_data;
    
    # Read file into Image::Magick
    my $magick = new Image::Magick( format => "png" );
    $status = $magick->Read( filename => $tmp_name );
    die "Error reading PNG input: $status" if $status;
    
    # Write file as JPEG to STDOUT
    $status = $magick->Write( "jpeg:-" );
    die "Error writing JPEG output: $status" if $status;
}
