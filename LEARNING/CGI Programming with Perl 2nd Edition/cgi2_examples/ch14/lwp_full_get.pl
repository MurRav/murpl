#!/usr/bin/perl -wT

use strict;
use LWP::UserAgent;
use HTTP::Request;

my $location = shift || die "Usage: $0 URL\n";

my $agent = new LWP::UserAgent;
my $req = new HTTP::Request GET => $location;
   $req->header('Accept' => 'text/html');

my $result = $agent->request( $req );

print $result->headers_as_string,
      $result->content;
