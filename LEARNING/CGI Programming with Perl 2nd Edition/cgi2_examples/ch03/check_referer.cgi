#!/usr/bin/perl -wT

use strict;

# The directory where images are stored; this shouldn't be in the 
# server's doc tree so users can't browse images except via this script
my $image_dir = "/usr/local/apache/data/images";

my $referer  = $ENV{HTTP_REFERER};
my $hostname = quotemeta( $ENV{HTTP_HOST} || $ENV{SERVER_NAME} );

if ( $referer and $referer !~ m|^http://$hostname/| ) {
    display_image( "copyright.gif" );
}
else {
    # Verify that the image name doesn't contain any unsafe characters
    my( $image_file ) = $ENV{PATH_INFO} =~ /^([\w+.]+)$/ or
        not_found();
    display_image( $image_file );
}

sub display_image {
    my $file = shift;
    my $full_path = "$image_dir/$file";
    
    # We'll simply report that the file isn't found if we can't open it
    open IMAGE, $full_path or not_found();
    
    print "Pragma: no-cache\n";
    print "Content-type: image/gif\n\n";
    
    binmode STDOUT;
    my $buffer = "";
    while ( read( IMAGE, $buffer, 16_384 ) ) {
        print $buffer;
    }
    close IMAGE;
}

sub not_found {
    print <<END_OF_ERROR;
Status: 404 Not Found
Content-type: text/html

<html>
<head>
  <title>File Not Found</title>
</head>

<body>
  <h1>File Not Found</h1>
  
  <p>Sorry, but you requested an image that could not be found. 
    Please check the URL you entered and try again.</p>
</body>
</html>
END_OF_ERROR
    
    exit;
}
