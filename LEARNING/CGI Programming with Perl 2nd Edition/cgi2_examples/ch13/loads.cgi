#!/usr/bin/perl -wT

use strict;

use CGI;
use GD;

BEGIN {
    $ENV{PATH} = '/bin:/usr/bin:/usr/ucb:/usr/local/bin';
    delete @ENV{ qw( IFS CDPATH ENV BASH_ENV ) };
}

use constant LOAD_MAX       => 10;

use constant IMAGE_SIZE     => 170;     # height and width
use constant GRAPH_SIZE     => 100;     # height and width
use constant TICK_LENGTH    => 3;

use constant ORIGIN_X_COORD => 30;
use constant ORIGIN_Y_COORD => 150;

use constant TITLE_TEXT     => "System Load Average";
use constant TITLE_X_COORD  => 10;
use constant TITLE_Y_COORD  => 15;

use constant AREA_COLOR     => ( 255, 0, 0 );
use constant AXIS_COLOR     => ( 0, 0, 0 );
use constant TEXT_COLOR     => ( 0, 0, 0 );
use constant BG_COLOR       => ( 255, 255, 255 );

my $q     = new CGI;
my @loads = get_loads();

print $q->header( -type => "image/png", -expires => "-1d" );

binmode STDOUT;
print area_graph( \@loads );


# Returns a list of the average loads from the system's uptime command
sub get_loads {
    my $uptime = `uptime` or die "Error running uptime: $!";
    my( $up_string ) = $uptime =~ /average: (.+)$/;
    my @loads = reverse
                map { $_ > LOAD_MAX ? LOAD_MAX : $_ }
                split /,\s*/, $up_string;
    @loads or die "Cannot parse response from uptime: $up_string";
    return @loads;
}


# Takes a one-dimensional list of data and returns an area graph as PNG
sub area_graph {
    my $data = shift;
    
    my $image = new GD::Image( IMAGE_SIZE, IMAGE_SIZE );
    my $background = $image->colorAllocate( BG_COLOR );
    my $area_color = $image->colorAllocate( AREA_COLOR );
    my $axis_color = $image->colorAllocate( AXIS_COLOR );
    my $text_color = $image->colorAllocate( TEXT_COLOR );
    
    # Add Title
    $image->string( gdLargeFont, TITLE_X_COORD, TITLE_Y_COORD,
                    TITLE_TEXT, $text_color );
    
    # Create polygon for data
    my $polygon = new GD::Polygon;
    $polygon->addPt( ORIGIN_X_COORD, ORIGIN_Y_COORD );
    
    for ( my $i = 0; $i < @$data; $i++ ) {
        $polygon->addPt( ORIGIN_X_COORD + GRAPH_SIZE / ( @$data - 1 ) * $i,
                         ORIGIN_Y_COORD - $$data[$i] * GRAPH_SIZE / LOAD_MAX );
    }
    
    $polygon->addPt( ORIGIN_X_COORD + GRAPH_SIZE, ORIGIN_Y_COORD );
    
    # Add Polygon
    $image->filledPolygon( $polygon, $area_color );
    
    # Add X Axis
    $image->line( ORIGIN_X_COORD, ORIGIN_Y_COORD,
                  ORIGIN_X_COORD + GRAPH_SIZE, ORIGIN_Y_COORD,
                  $axis_color );
    # Add Y Axis
    $image->line( ORIGIN_X_COORD, ORIGIN_Y_COORD,
                  ORIGIN_X_COORD, ORIGIN_Y_COORD - GRAPH_SIZE,
                  $axis_color );
    
    # Add X Axis Ticks Marks
    for ( my $x = 0; $x <= GRAPH_SIZE; $x += GRAPH_SIZE / ( @$data - 1 ) ) {
        $image->line( $x + ORIGIN_X_COORD, ORIGIN_Y_COORD - TICK_LENGTH,
                      $x + ORIGIN_X_COORD, ORIGIN_Y_COORD + TICK_LENGTH,
                      $axis_color );
    }
    
    # Add Y Axis Tick Marks
    for ( my $y = 0; $y <= GRAPH_SIZE; $y += GRAPH_SIZE / LOAD_MAX ) {
        $image->line( ORIGIN_X_COORD - TICK_LENGTH, ORIGIN_Y_COORD - $y,
                      ORIGIN_X_COORD + TICK_LENGTH, ORIGIN_Y_COORD - $y,
                      $axis_color );
    }
    
    $image->transparent( $background );
    
    return $image->png;
}
