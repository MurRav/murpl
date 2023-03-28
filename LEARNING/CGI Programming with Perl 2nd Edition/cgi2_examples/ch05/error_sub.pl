#!/usr/bin/perl -wT

use strict;

sub error {
    my( $q, $error_message ) = @_;
    
    print $q->header( "text/html" ),
          $q->start_html( "Error" ),
          $q->h1( "Error" ),
          $q->p( "Sorry, the following error has occurred: " );
          $q->p( $q->i( $error_message ) ),
          $q->end_html;
    exit;
}
