#!/usr/bin/perl -wT

use strict;
use CGI qw( :standard );

my $name = param( "name" );

print header( "text/html" ),
      start_html( "Welcome" ),
      p( "Hi $name!" ),
      end_html;
