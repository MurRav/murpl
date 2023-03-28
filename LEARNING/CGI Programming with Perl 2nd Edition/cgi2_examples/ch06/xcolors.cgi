#!/usr/bin/perl -wT

use strict;
use HTML::Template;

my $rgb_file = "/usr/X11/lib/X11/rgb.txt";
my $template = "/usr/local/apache/templates/xcolors.tmpl";

my @colors   = parse_colors( $rgb_file );

print "Content-type: text/html\n\n";
my $tmpl = new HTML::Template( filename => $template );

$tmpl->param( colors => \@colors );
print $tmpl->output;


sub parse_colors {
    my $path = shift;
    local *RGB_FILE;
    open RGB_FILE, $path or die "Cannot open $path: $!";
    
    while (<RGB_FILE>) {
        next if /^!/;
        chomp;
        my( $r, $g, $b, $name ) = split;
        
        # Convert to hexadecimal #RRGGBB format
        my $rgb = sprintf "#%0.2x%0.2x%0.2x", $r, $g, $b;
        
        my %color = ( rgb => $rgb, name => $name );
        push @colors, \%color;
    }
    
    close RGB_FILE;
    return @colors;
}
