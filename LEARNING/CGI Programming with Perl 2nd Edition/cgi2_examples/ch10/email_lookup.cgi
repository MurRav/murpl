#!/usr/bin/perl -wT

use strict;
use DB_File;
use Fcntl;
use CGI;

my $q        = new CGI;
my $username = $q->param( "user" );
my $dbm_file = "/usr/local/apache/data/user_email.db";
my %dbm_hash;
my $email;

tie %dbm_hash, "DB_File", $dbm_file, O_RDONLY or
    die "Unable to open dbm file $dbm_file: $!";

if ( exists $dbm_hash{$username} ) {
    $email = $q->a( { href => "mailto:$dbm_hash{$username}" },
                    $dbm_hash{$username} );
}
else {
    $email = "Username not found";
}

untie %dbm_hash;

print $q->header( "text/html" ),
      $q->start_html( "Email Lookup Results" ),
      $q->h2( "Email Lookup Results" ),
      $q->hr,
      $q->p( "Here is the email address for the username you requested: " ),
      $q->p( "Username: $username", $q->br,
             "Email: $email" ),
      $q->end_html; 
