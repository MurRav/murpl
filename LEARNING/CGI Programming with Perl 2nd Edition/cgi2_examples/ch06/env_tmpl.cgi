#!/usr/bin/perl -wT

use strict;
use HTML::Template;

use constant TMPL_FILE => "$ENV{DOCUMENT_ROOT}/templates/env.tmpl";

my $tmpl = new HTML::Template( filename => TMPL_FILE,
                               no_includes => 1 );
my @env;

foreach ( sort keys %ENV ) {
    push @env, { var_name => $_, var_value => $ENV{$_} };
}

$tmpl->param( env => \@env );

print "Content-type: text/html\n\n",
      $tmpl->output;
