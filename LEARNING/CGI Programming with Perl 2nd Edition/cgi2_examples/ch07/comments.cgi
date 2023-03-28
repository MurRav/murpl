#!/usr/bin/perl -wT

use strict;

use CGI;
use DB_File;
use Fcntl qw( :DEFAULT :flock );

my $DBM_FILE = "/usr/local/httpd/data/bookmarklets/comments.dbm";

my $q       = new CGI;
my $url     = $q->param( "url" );
my $comment;

if ( defined $q->param( "save" ) ) {
    $comment = $q->param( "comment" ) || "";
    save_comment( $url, $comment );
}
else {
    $comment = get_comment( $url );
}

print $q->header( "text/html" ),
      $q->start_html( -title => $url, -bgcolor => "white" ),
      $q->start_form( { action => "/cgi/comments.cgi" } ),
      $q->hidden( "url" ),
      $q->textarea( -cols => 20, -rows => 8, -value => $comment ),
      $q->div( { -align => "right" },
          $q->submit( -name => "save", -value => "Save Comment" )
      ),
      $q->end_form,
      $q->end_html;


sub get_comment {
    my( $url ) = @_;
    my %dbm;
    
    tie %dbm, "DB_File", $DBM_FILE, O_RDONLY | O_CREAT or
        die "Unable to read from $DBM_FILE: $!";
    return $dbm{$url};
}


sub set_comment {
    my( $url, $comment ) = @_;
    my %dbm;
    
    tie %dbm, "DB_File", $DBM_FILE, O_RDWR | O_CREAT or
        die "Unable to write to $DBM_FILE: $!";
    $dbm{$url} = $comment;
}
