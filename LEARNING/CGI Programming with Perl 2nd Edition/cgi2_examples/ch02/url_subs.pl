#!/usr/bin/perl -wT

use strict;

sub url_encode {
    my $text = shift;
    $text =~ s/([^a-z0-9_.!~*'() -])/sprintf "%%%02X", ord($1)/egi;
    $text =~ tr/ /+/;
    return $text;
}


sub url_decode {
    my $text = shift;
    $text =~ tr/\+/ /;
    $text =~ s/%([a-f0-9][a-f0-9])/chr( hex( $1 ) )/egi;
    return $text;
}
