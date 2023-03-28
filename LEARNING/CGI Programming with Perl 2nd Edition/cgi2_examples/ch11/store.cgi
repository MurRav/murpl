#!/usr/bin/perl -w

use strict;
use CGI;

my $q       = new CGI;
my $cart_id = $q->cookie( -name => "cart_id" ) || set_cookie( $q );

# Script continues for users with cookies
# .
# .


sub set_cookie {
    my $q = shift;
    my $server = $q->server_name;
    my $cart_id = unique_id();
    my $cookie  = $q->cookie( -name  => "cart_id",
                              -value => $cart_id,
                              -path  => "/cgi/store" );
    print "Location: http://$server/cgi/store/cookie_test.cgi\n",
          "Set-Cookie: $cookie\n\n";
    exit;
}
