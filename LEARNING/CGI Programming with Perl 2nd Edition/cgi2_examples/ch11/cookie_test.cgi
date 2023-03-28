#!/usr/bin/perl -wT

use strict;
use CGI;

use constant SOURCE_CGI => "/cgi/main.cgi";

my $q      = new CGI;
my $cookie = $q->cookie( -name => "cart_id" );

if ( defined $cookie ) {
    print $q->redirect( SOURCE_CGI );
}
else {
    print $q->header( -type => "text/html", -expires => "-1d" ),
          $q->start_html( "Cookies Disabled" ),
          $q->h1( "Cookies Disabled" ),
          $q->p( "Your browser is not accepting cookies. Please upgrade ",
                 "to a newer browser or enable cookies in your preferences and",
            $q->a( { -href => SOURCE_CGI }, "return to the store" ),
            "."
          ),
          $q->end_html;
}
