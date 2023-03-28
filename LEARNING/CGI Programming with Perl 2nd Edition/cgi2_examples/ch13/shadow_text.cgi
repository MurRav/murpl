#!/usr/bin/perl -w

use strict;

use CGI;
use Image::Magick;

use constant FONTS_DIR => "/usr/local/httpd/fonts";

my $q      = new CGI;
my $font   = $q->param( "font" )  || 'cetus';
my $size   = $q->param( "size" )  || 40;
my $string = $q->param( "text" )  || 'Hello!';
my $color  = $q->param( "color" ) || 'black';

$font   =~ s/\W//g;
$font   = 'bodiac' unless -e FONTS_DIR . "/$font.ttf";

my $image = new Image::Magick( size => '500x100' );

$image->Read( 'xc:white' );
$image->Annotate( font      => "\@@{[ FONTS_DIR ]}/$font.ttf", 
                  pen       => 'gray',
                  pointsize => $size,
                  gravity   => 'Center',
                  text      => $string );

$image->Blur( 100 );

$image->Roll( "+5+5" );

$image->Annotate( font      => "\@@{[ FONTS_DIR ]}/$font.ttf", 
                  pen       => $color,
                  pointsize => $size,
                  gravity   => 'Center',
                  text      => $string );

binmode STDOUT;
print $q->header( "image/jpeg" );
$image->Write( "jpeg:-" );
