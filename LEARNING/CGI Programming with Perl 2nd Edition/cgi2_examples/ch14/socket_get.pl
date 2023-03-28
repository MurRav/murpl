#!/usr/bin/perl -wT

use strict;

use IO::Socket;
use URI;

my $location = shift || die "Usage: $0 URL\n";

my $url      = new URI( $location );
my $host     = $url->host;
my $port     = $url->port || 80;
my $path     = $url->path || "/";

my $socket   = new IO::Socket::INET (PeerAddr => $host,
                                     PeerPort => $port,
                                     Proto    => 'tcp')
               or die "Cannot connect to the server.\n";

$socket->autoflush (1);

print $socket "GET $path HTTP/1.1\n",
              "Host: $host\n\n";
print while (<$socket>);

$socket->close;
