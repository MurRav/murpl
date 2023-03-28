#!/usr/bin/perl -w

use strict;

use LWP::UserAgent;
use HTTP::Request;
use HTTP::Headers;
use CGI;

my $q = new CGI( {
    price    => 0.01,
    name     => "Super Blaster 3000",
    quantity => 1,
    submit   => "Order",
} );

my $form_data = $q->query_string;

my $headers = new HTTP::Headers(
    Accept       => "text/html, text/plain, image/*",
    Referer      => "http://localhost/products/sb3000.html",
    Content_Type => "application/x-www-form-urlencoded"
);

my $request = new HTTP::Request(
    "POST",
    "http://localhost/cgi/feedback.cgi",
    $headers
);

$request->content( $form_data );

my $agent = new LWP::UserAgent;
$agent->agent( "Mozilla/4.5" );
my $response = $agent->request( $request );

print $response->content;
