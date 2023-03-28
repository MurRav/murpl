#!/usr/bin/perl -wT

use strict;
use Fcntl qw( :DEFAULT :flock );
use DB_File;

use constant COUNT_FILE => "/usr/local/apache/data/counter/count.dbm";
my %count;
my $url = $ENV{DOCUMENT_URI};
local *DBM;

print "Content-type: text/plain\n\n";

if ( my $db = tie %count, "DB_File", COUNT_FILE, O_RDWR | O_CREAT ) {
    my $fd = $db->fd;
    open DBM, "+<&=$fd" or die "Could not dup DBM for lock: $!";
    flock DBM, LOCK_EX;
    undef $db;
    $count{$url} = 0 unless exists $count{$url};
    my $num_hits = ++$count{$url};
    untie %count;
    close DBM;
    print "$num_hits\n";
} else {
    print "[Error processing counter data]\n";
}
