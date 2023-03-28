#!/usr/bin/perl -wT
# WARNING: This code has significant limitations; see description

use strict;
use CGI;
use CGIBook::Error;

# Make the environment safe to call fgrep
BEGIN {
    $ENV{PATH} = "/bin:/usr/bin";
    delete @ENV{ qw( IFS CDPATH ENV BASH_ENV ) };
}

my $FGREP         = "/usr/local/bin/fgrep";
my $DOCUMENT_ROOT = $ENV{DOCUMENT_ROOT};
my $VIRTUAL_PATH  = "";

my $q       = new CGI;
my $query   = $q->param( "query" );

$query =~ s/[^\w ]//g;
$query =~ /([\w ]+)/;
$query = $1;

unless ( defined $query ) {
    error( $q, "Please specify a valid query!" );
}

my $results = search( $q, $query );

print $q->header( "text/html" ),
      $q->start_html( "Simple Search with fgrep" ),
      $q->h1( "Search for: $query" ),
      $q->ul( $results || "No matches found" ),
      $q->end_html;


sub search {
    my( $q, $query ) = @_;
    local *PIPE;
    my $matches = "";
    
    open PIPE, "$FGREP -il '$query' $DOCUMENT_ROOT/* |"
        or die "Cannot open fgrep: $!";
    
    while ( <PIPE> ) {
        chomp;
        s|.*/||;
        $matches .= $q->li(
                        $q->a( { href => "$VIRTUAL_PATH/$_" }, $_ )
                    );
    }
    close PIPE;
    return $matches;
}
