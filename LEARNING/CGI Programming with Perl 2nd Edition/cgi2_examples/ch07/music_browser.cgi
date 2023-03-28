#!/usr/bin/perl -wT

use strict;
use WDDX;
use HTML::Template;

use constant DATA_FILE => "/usr/local/httpd/data/music/music_data.txt";
use constant TEMPLATE  => "/usr/local/httpd/templates/music/music_browser.tmpl";

print "Content-type: text/html\n\n";

my $wddx = new WDDX;
my $rec = build_recordset( $wddx, DATA_FILE );
my $js_rec = $rec->as_javascript( "data" );

my $tmpl = new HTML::Template( filename => TEMPLATE );
$tmpl->param( song_data => $js_rec );

print $tmpl->output;


sub build_recordset {
    my( $wddx, $file ) = @_;
    local *FILE;
    
    open FILE, $file or die "Cannot open $file: $!";
    my $headings = <FILE>;
    chomp $headings;
    my @field_names = split "\t", lc $headings;
    my @types = map "string", @field_names;
    
    my $rec = $wddx->recordset( \@field_names, \@types );
    
    while (<FILE>) {
    	chomp;
    	my @fields = split "\t";
    	$rec->add_row( \@fields );
    }
    
    close FILE;
    return $rec;
}
