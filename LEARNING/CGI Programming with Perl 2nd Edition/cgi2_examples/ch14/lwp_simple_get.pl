#!/usr/bin/perl -wT

use strict;
use LWP::Simple;

my $location = shift || die "Usage: $0 URL\n";

getprint( $location );
