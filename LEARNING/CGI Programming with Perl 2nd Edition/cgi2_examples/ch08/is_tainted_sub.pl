#!/usr/bin/perl -wT

use strict;

sub is_tainted {
    my $var = shift;
    my $blank = substr( $var, 0, 0 );
    return not eval { eval "1 || $blank" || 1 };
}
