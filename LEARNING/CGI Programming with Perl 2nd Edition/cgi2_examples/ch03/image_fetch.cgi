#!/usr/bin/perl -wT

use strict;

my $image_type = $ENV{HTTP_ACCEPT} =~ m|image/png| ? "png" : "jpeg";
my( $basename ) = $ENV{PATH_INFO} =~ /(\w+)/;
my $image_path = "$ENV{DOCUMENT_ROOT}/images/$basename.$image_type";

unless ( $basename and -B $image_path and open IMAGE, $image_path ) {
    print "Location: /errors/not_found.html\n\n";
    exit;
}

my $buffer;
print "Content-type: image/$image_type\n\n";
binmode STDOUT;

while ( read( IMAGE, $buffer, 16_384 ) ) {
    print $buffer;
}
