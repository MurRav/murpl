#!/usr/bin/perl -wT

use strict;
use CGI;
use CGI::Carp;

use constant BUFFER_SIZE     => 4_096;
use constant IMAGE_DIRECTORY => "/usr/local/apache/data/random-images";

my $q = new CGI;
my $buffer = "";

my $image = random_file( IMAGE_DIRECTORY, '\\.(png|jpg|gif)$' );
my( $type ) = $image =~ /\.(\w+)$/;
$type eq "jpg" and $type = "jpeg";

print $q->header( -type => "image/$type", -expires => "-1d" );
binmode STDOUT;

local *IMAGE;
open IMAGE, IMAGE_DIRECTORY . "/$image" or die "Cannot open file $image: $!";
while ( read( IMAGE, $buffer, BUFFER_SIZE ) ) {
    print $buffer;
}
close IMAGE;


# Takes a path to a directory and an optional filename mask regex
# Returns the name of a random file from the directory
sub random_file {
    my( $dir, $mask ) = @_;
    my $i = 0;
    my $file;
    local( *DIR, $_ );
    
    opendir DIR, $dir or die "Cannot open $dir: $!";
    while ( defined ( $_ = readdir DIR ) ) {
        /$mask/o or next if defined $mask;
        rand ++$i < 1 and $file = $_;
    }
    closedir DIR;
    return $file;
}
