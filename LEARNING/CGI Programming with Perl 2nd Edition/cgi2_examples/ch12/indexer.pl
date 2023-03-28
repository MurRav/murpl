#!/usr/bin/perl -wT
# This is not a CGI, so taint mode not required

use strict;

use File::Find;
use DB_File;
use Getopt::Long;
use Text::English;
use Fcntl;

use constant DB_CACHE      => 0;
use constant DEFAULT_INDEX => "/usr/local/apache/data/index.db";

my( %opts, %index, @files, $stop_words );

GetOptions( \%opts, "dir=s",
                    "cache=s",
                    "index=s",
                    "ignore",
                    "stop=s",
                    "numbers",
                    "stem" );

die usage() unless $opts{dir} && -d $opts{dir};

$opts{'index'}        ||= DEFAULT_INDEX;
$DB_BTREE->{cachesize}  = $opts{cache} || DB_CACHE;

$index{"!OPTION:stem"}   = 1 if $opts{'stem'};
$index{"!OPTION:ignore"} = 1 if $opts{'ignore'};

tie %index, "DB_File", $opts{'index'}, O_RDWR|O_CREAT, 0640
    or die "Cannot tie database: $!\n";

find( sub { push @files, $File::Find::name }, $opts{dir} );
$stop_words = load_stopwords( $opts{stop} ) if $opts{stop};

process_files( \%index, \@files, \%opts, $stop_words );

untie %index;


sub load_stopwords {
    my $file = shift;
    my $words = {};
    local( *INFO, $_ );
    
    die "Cannot file stop file: $file\n" unless -e $file;
    
    open INFO, $file or die "$!\n";
    while ( <INFO> ) {
        next if /^#/;
        $words->{lc $1} = 1 if /(\S+)/;
    }
    
    close INFO;    
    return $words;
}

sub process_files {
    my( $index, $files, $opts, $stop_words ) = @_;
    local( *FILE, $_ );
    local $/ = "\n\n";
    
    for ( my $file_id = 0; $file_id < @$files; $file_id++ ) {
        my $file = $files[$file_id];
        my %seen_in_file;
        
        next unless -T $file;
        
        print STDERR "Indexing $file\n";
        $index->{"!FILE_NAME:$file_id"} = $file;
        
        open FILE, $file or die "Cannot open file: $file!\n";
        
        while ( <FILE> ) {
            
            tr/A-Z/a-z/ if $opts{ignore};
            s/<.+?>//gs; # Note this doesn't handle < or > in comments or js
            
            while ( /([a-z\d]{2,})\b/gi ) {
                my $word = $1;
                next if $stop_words->{lc $word};
                next if $word =~ /^\d+$/ && not $opts{number};
                
                ( $word ) = Text::English::stem( $word ) if $opts{stem};
                
                $index->{$word} = ( exists $index->{$word} ? 
                    "$index->{$word}:" : "" ) . "$file_id" unless 
                    $seen_in_file{$word}++;
            }
        }
    }
}

sub usage {
    my $usage = <<End_of_Usage;

Usage: $0 -dir directory [options]

The options are:

  -cache         DB_File cache size (in bytes)
  -index         Path to index, default:/usr/local/apache/data/index.db
  -ignore        Case-insensitive index
  -stop          Path to stopwords file
  -numbers       Include numbers in index
  -stem          Stem words

End_of_Usage
    return $usage;
}
