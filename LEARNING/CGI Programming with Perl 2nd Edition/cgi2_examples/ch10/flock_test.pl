#!/usr/bin/perl -wT

use IO::File;
use Fcntl ":flock";

*FH1 = new_tmpfile IO::File or die "Cannot open temporary file: $!\n";

eval { flock FH1, LOCK_SH };
$@ and die "It does not look like your system supports flock: $@\n";

open FH2, ">> &FH1" or die "Cannot dup filehandle: $!\n";

if ( flock FH2, LOCK_SH | LOCK_NB ) {
    print "Your system supports shared file locks\n";
}
else {
    print "Your system only supports exclusive file locks\n";
}
