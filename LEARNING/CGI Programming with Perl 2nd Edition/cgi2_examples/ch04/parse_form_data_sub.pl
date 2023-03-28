#!/usr/bin/perl -wT

use strict;

sub parse_form_data {
    my %form_data;
    my $name_value;
    my @name_value_pairs = split /&/, $ENV{QUERY_STRING};
    
    if ( $ENV{REQUEST_METHOD} eq 'POST' ) {
        my $query = "";
        read( STDIN, $query, $ENV{CONTENT_LENGTH} ) == $ENV{CONTENT_LENGTH}
          or return undef;
        push @name_value_pairs, split /&/, $query;
    }
    
    foreach $name_value ( @name_value_pairs ) {
        my( $name, $value ) = split /=/, $name_value;
        
        $name =~ tr/+/ /;
        $name =~ s/%([\da-f][\da-f])/chr( hex($1) )/egi;
        
        $value = "" unless defined $value;
        $value =~ tr/+/ /;
        $value =~ s/%([\da-f][\da-f])/chr( hex($1) )/egi;
        
        $form_data{$name} = $value;
    }
    return %form_data;
}
