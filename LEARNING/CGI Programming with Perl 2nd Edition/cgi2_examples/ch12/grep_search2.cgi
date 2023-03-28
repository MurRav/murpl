#!/usr/bin/perl -wT

use strict;
use CGI;
use CGIBook::Error;

my $DOCUMENT_ROOT = $ENV{DOCUMENT_ROOT};
my $VIRTUAL_PATH  = "";

my $q           = new CGI;
my $query       = $q->param( "query" );

if ( defined $query and length $query ) {
    error( $q, "Please specify a valid query!" );
}

$query = quotemeta( $query );
my $results = search( $q, $query );

print $q->header( "text/html" ),
      $q->start_html( "Simple Perl Search" ),
      $q->h1( "Search for: $query" ),
      $q->ul( $results || "No matches found" ),
      $q->end_html;


sub search {
    my( $q, $query ) = @_;
    my( %matches, @files, @sorted_paths, $results );
    
    local( *DIR, *FILE );
    
    opendir DIR, $DOCUMENT_ROOT or
        error( $q, "Cannot access search dir!" );
        
    @files = grep { -T "$DOCUMENT_ROOT/$_" } readdir DIR;
    close DIR;
    
    my $file;
    foreach $file ( @files ) {
        my $full_path = "$DOCUMENT_ROOT/$_";
        
        open FILE, $full_path or
            error( $q, "Cannot process $file!" );
        
        while ( <FILE> ) {
            if ( /$query/io ) {
                $_ = html_escape( $_ );
                s|$query|<B>$query</B>|gio;
                push @{ $matches{$full_path}{content} }, $_;
                $matches{$full_path}{file} = $file;
                $matches{$full_path}{num_matches}++;
            }
        }
        close FILE;
    }
    
    @sorted_paths = sort {
                        $matches{$b}{num_matches} <=>
                        $matches{$a}{num_matches} ||
                        $a cmp $b
                    } keys %matches;
    
    my $full_path;
    foreach $full_path ( @sorted_paths ) {
        my $file        = $matches{$full_path}{file};
        my $num_matches = $matches{$full_path}{num_matches};
        
        my $link = $q->a( { -href => "$VIRTUAL_PATH/$file" }, $file );
        my $content = join $q->br, @{ $matches{$full_path}{content} };
        
        $results .= $q->p( $q->b( $link ) . " ($num_matches matches)" .
                           $q->br . $content
                    );
    }
    
    return $results;
}


sub html_escape {
    my( $text ) = @_;
    
    $text =~ s/&/&amp;/g;
    $text =~ s/</&lt;/g;
    $text =~ s/>/&gt;/g;
}
