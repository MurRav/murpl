#!/usr/bin/perl -wT

use strict;
use Fcntl ":flock";
use CGI;
use CGIBook::Error;

my $DATA_FILE = "/usr/local/apache/data/tab_delimited_records.txt";

my $q       = new CGI;
my $name    = $q->param( "name" );
my $comment = substr( $q->param( "comment" ), 0, 80 );

unless ( $name ) {
    error( $q, "Please enter your name." );
}

open DATA_FILE, ">> $DATA_FILE" or die "Cannot append to $DATA_FILE: $!";
flock DATA_FILE, LOCK_EX;
seek DATA_FILE, 0, 2;

print DATA_FILE encode_data( $name, $comment );
close DATA_FILE;

print $q->header( "text/html" ),
      $q->start_html( "Our Petition" ),
      $q->h2( "Thank You!" ),
      $q->p( "Thank you for signing our petition. ",
             "Your name has been been added below:" ),
      $q->hr,
      $q->start_table,
      $q->tr( $q->th( "Name", "Comment" ) );
      
open DATA_FILE, $DATA_FILE or die "Cannot read $DATA_FILE: $!";
while (<DATA_FILE>) {
    my @data = decode_data( $_ );
    print $q->tr( $q->td( @data ) );
}
close DATA_FILE;

print $q->end_table,
      $q->end_html;


sub encode_data {
    my @fields = map {
        s/\\/\\\\/g;
        s/\t/\\t/g;
        s/\n/\\n/g;
        s/\r/\\r/g;
        $_;
    } @_;
    
    my $line = join "\t", @fields;
    return $line . "\n";
}

sub decode_data {
    my $line = shift;
    
    chomp $line;
    my @fields = split /\t/, $line;
    
    return map {
        s/\\(.)/$1 eq 't' and "\t" or
                $1 eq 'n' and "\n" or
                $1 eq 'r' and "\r" or
                "$1"/eg;
        $_;
    } @fields;
}
